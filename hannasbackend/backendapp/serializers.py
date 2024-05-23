from rest_framework import serializers
from .models import Company, UserProfile, ReportTemplate, Question, Report, Answer


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "question", "report", "answer", "explanation", "company"]


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True, source="answer_set")

    class Meta:
        model = Question
        fields = ["id", "text", "template", "company", "answers"]


class ReportSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(
        many=True, read_only=True, source="template.questions"
    )

    class Meta:
        model = Report
        fields = [
            "id",
            "report_title",
            "submitted_on",
            "last_updated",
            "submitted_by",
            "company",
            "questions",
        ]


class ReportTemplateSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    reports = ReportSerializer(many=True, read_only=True, source="report_set")

    class Meta:
        model = ReportTemplate
        fields = ["id", "name", "accessible_by", "company", "questions", "reports"]
