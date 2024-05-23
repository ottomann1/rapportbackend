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


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "text", "template", "company"]


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = [
            "id",
            "report_title",
            "submitted_on",
            "last_updated",
            "submitted_by",
            "company",
        ]


class ReportTemplateSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    reports = ReportSerializer(many=True, read_only=True, source="report_set")

    class Meta:
        model = ReportTemplate
        fields = ["id", "name", "accessible_by", "company", "questions", "reports"]


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"
