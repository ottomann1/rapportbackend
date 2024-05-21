from django.contrib import admin
from .models import Report, Question, Answer, ReportTemplate

admin.site.register(Report)
admin.site.register(ReportTemplate)
admin.site.register(Question)
admin.site.register(Answer)
