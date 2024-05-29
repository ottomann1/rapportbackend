from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.urls import path
from django.contrib.auth.models import User, Group
from .forms import ReportForm, ReportTemplateForm
from rest_framework import viewsets
from .models import Company, UserProfile, ReportTemplate, Question, Report, Answer
from .serializers import (
    CompanySerializer,
    UserProfileSerializer,
    ReportTemplateSerializer,
    QuestionSerializer,
    ReportSerializer,
    AnswerSerializer,
)
from .permissions import IsSuperAdmin, IsAdmin, IsUser, IsOwnerOrReadOnly
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_info(request):
    user = request.user
    return Response(
        {
            "username": user.username,
            "company": user.profile.company.name,  # Assuming a profile model with a company relationship
        }
    )


@api_view(["POST"])
def register_user(request):
    username = request.data.get("username")
    password = request.data.get("password")
    role = request.data.get("role")  # 'superadmin', 'admin', or 'user'

    if username is None or password is None or role is None:
        return Response(
            {"error": "Please provide username, password, and role"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(username=username, password=password)
    group = Group.objects.get(name=role)
    user.groups.add(group)

    return Response(
        {"message": "User created successfully"}, status=status.HTTP_201_CREATED
    )


@login_required
def home(request):
    return render(request, "home.html")


def user_is_company_admin(user):
    # Implement logic to check if the user is an admin of their company
    return (
        user.userprofile.is_admin
    )  # Example attribute, adjust according to your model


@login_required
def report_detail(request, report_id):
    report = Report.objects.get(id=report_id)
    return render(request, "report_detail.html", {"report": report})


def view_report(request, report_id):
    report = Report.objects.get(id=report_id)
    questions_with_answers = []
    print("omg")
    for question in report.template.questions.all():
        print(question)
        answers = question.answers.filter(report=report)
        questions_with_answers.append((question, answers))

    return render(
        request,
        "report_detail.html",
        {"report": report, "questions_with_answers": questions_with_answers},
    )


def profile_view(request):
    user_reports = Report.objects.filter(submitted_by=request.user)
    return render(request, "profile.html", {"reports": user_reports})


def report_list(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        reports = Report.objects.filter(company=user_profile.company)
    except UserProfile.DoesNotExist:
        reports = Report.objects.none()  # Or handle as appropriate

    return render(request, "reports/report_list.html", {"reports": reports})


def create_report_template(request):
    if request.method == "POST":
        form = ReportTemplateForm(request.POST)
        formset = QuestionFormset(request.POST)
        if form.is_valid() and formset.is_valid():
            report_template = form.save()
            formset.instance = report_template
            formset.save()
            # Redirect or handle as needed
    else:
        form = ReportTemplateForm()
        formset = QuestionFormset()

    return render(
        request, "create_report_template.html", {"form": form, "formset": formset}
    )


def update_report_template(request, template_id):
    template = get_object_or_404(ReportTemplate, id=template_id)
    if request.method == "POST":
        form = ReportTemplateForm(request.POST, instance=template)
        formset = QuestionFormset(request.POST, instance=template)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            # return redirect("some_view")  # Redirect to the desired view after update
    else:
        form = ReportTemplateForm(instance=template)
        formset = QuestionFormset(instance=template)

    return render(
        request,
        "update_report_template.html",
        {"form": form, "formset": formset, "template": template},
    )


def get_template_questions(request, template_id):
    template = get_object_or_404(ReportTemplate, id=template_id)
    questions = template.questions.all().values("id", "text")
    return JsonResponse(list(questions), safe=False)


def create_report(request):
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save()
            for key, value in request.POST.items():
                if key.startswith("answer_"):
                    question_id = key.split("_")[1]
                    question = Question.objects.get(id=question_id)
                    explanation_key = "explanation_" + question_id
                    explanation = request.POST.get(explanation_key, "")
                    Answer.objects.create(
                        report=report,
                        question=question,
                        answer=value,
                        explanation=explanation,
                    )
            return redirect(
                "some_success_url"
            )  # Redirect to a success page or the report detail view
    else:
        form = ReportForm()

    return render(request, "create_report.html", {"form": form})


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class ReportTemplateViewSet(viewsets.ModelViewSet):
    queryset = ReportTemplate.objects.all()
    serializer_class = ReportTemplateSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()  # Add this line
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="superadmin").exists():
            return Report.objects.all()
        elif user.groups.filter(name="admin").exists():
            return Report.objects.filter(company=user.profile.company)
        else:
            return Report.objects.filter(submitted_by=user)

    def perform_create(self, serializer):
        serializer.save(
            submitted_by=self.request.user, company=self.request.user.profile.company
        )


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
