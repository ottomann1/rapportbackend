from rest_framework import serializers
from .models import Report, ReportTemplate, Question, Answer


class AnswerSerializer(serializers.ModelSerializer):
    question = serializers.ReadOnlyField(source="question.text")

    class Meta:
        model = Answer
        fields = ["question", "answer", "explanation"]


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ["id", "text", "answers"]


class ReportSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Report
        fields = [
            "id",
            "report_title",
            "submitted_on",
            "last_updated",
            "template",
            "answers",
        ]


class ReportTemplateSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    reports = ReportSerializer(many=True, read_only=True)

    class Meta:
        model = ReportTemplate
        fields = ["id", "name", "questions", "reports"]
