from django import forms
from django.forms import inlineformset_factory
from .models import Report, ReportTemplate, Question


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = "__all__"


class ReportTemplateForm(forms.ModelForm):
    class Meta:
        model = ReportTemplate
        fields = ["name"]


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["text"]


QuestionFormset = inlineformset_factory(
    ReportTemplate, Question, form=QuestionForm, extra=0, can_delete=True
)
