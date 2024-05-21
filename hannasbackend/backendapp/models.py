from django.db import models
from django.conf import settings


class Company(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    is_company_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class ReportTemplate(models.Model):
    name = models.CharField(max_length=100)
    accessible_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="accessible_templates"
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)

    # Add any other fields that might describe the template


class Question(models.Model):
    text = models.TextField()
    template = models.ForeignKey(
        ReportTemplate, related_name="questions", on_delete=models.CASCADE
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)

    # This sets up a many-to-one relationship to ReportTemplate


class Report(models.Model):
    report_title = models.CharField(max_length=100)
    submitted_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    template = models.ForeignKey(ReportTemplate, on_delete=models.SET_NULL, null=True)
    submitted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name="submitted_reports",
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    # Include any other relevant fields


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, related_name="answers", on_delete=models.CASCADE)
    answer = models.CharField(max_length=255)  # or whatever field type you need
    explanation = models.TextField(blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
