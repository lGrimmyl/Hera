
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IncidentReportViewSet, CustomUserView, CreateUserView

router = DefaultRouter()
router.register(r'police-reports', IncidentReportViewSet)

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
    path('create_user/', CreateUserView.as_view(), name='create_user'),
    path('me/', CustomUserView.as_view(), name='User Information'),
     path('me/change-password/', CustomUserView.as_view(), name='custom-change-password'),
]