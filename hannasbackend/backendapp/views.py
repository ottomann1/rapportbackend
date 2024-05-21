from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import (
    Report,
    Question,
    Answer,
    ReportTemplate,
    UserProfile,
)  # Import your models as needed
from .forms import ReportForm, ReportTemplateForm, QuestionFormset
from rest_framework import viewsets
from .serializers import ReportSerializer, ReportTemplateSerializer


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


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class ReportTemplateViewSet(viewsets.ModelViewSet):
    queryset = ReportTemplate.objects.all()
    serializer_class = ReportTemplateSerializer
