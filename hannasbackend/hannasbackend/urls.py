"""
URL configuration for hannasbackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.contrib.auth import views as auth_views
from backendapp import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backendapp.views import (
    CompanyViewSet,
    UserProfileViewSet,
    ReportTemplateViewSet,
    QuestionViewSet,
    ReportViewSet,
    AnswerViewSet,
    user_info,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r"companies", CompanyViewSet)
router.register(r"userprofiles", UserProfileViewSet)
router.register(r"reporttemplates", ReportTemplateViewSet)
router.register(r"questions", QuestionViewSet)
router.register(r"reports", ReportViewSet, basename="report")
router.register(r"answers", AnswerViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/user/", user_info),
    path("admin/", admin.site.urls),
    path(
        "create-report-template/",
        views.create_report_template,
        name="create_report_template",
    ),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "update-report-template/<int:template_id>/",
        views.update_report_template,
        name="update_report_template",
    ),
    path(
        "get-template-questions/<int:template_id>/",
        views.get_template_questions,
        name="get_template_questions",
    ),
    path("accounts/profile/", views.profile_view, name="profile"),
    path("", views.home, name="home"),
    path("create-report/", views.create_report, name="create_report"),
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
]
