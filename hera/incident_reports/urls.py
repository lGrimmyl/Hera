from django.contrib import admin
from django.urls import path
from .views import ReportListView, ReportCreateView, ReportDetailView, ReportSuspectCreateView, ReportVictimCreateView, ReportChildConflictCreateView,CombinedReportMetricsView, DailyReportCountView, ReportsNeedingResponseView, ResolvedReportsCountView,EmergencyReportCountView, update_report_status
from incident_reports import views

urlpatterns = [
    path('reports/', ReportListView.as_view(), name='report-list'),
    path('reports/create/', ReportCreateView.as_view(), name='report-create'),
    path('reports/<int:pk>/', ReportDetailView.as_view(), name='report-detail'),
    #Incident Reports
    path('reports/suspect/', ReportSuspectCreateView.as_view(), name='suspect-information'),
    path('reports/victim/', ReportVictimCreateView.as_view(), name='victim-information'),
    path('reports/childconflict/', ReportChildConflictCreateView.as_view(), name='guardian-information'),
    path('reports/emergency/', views.create_emergency_report, name='create-emergency-report'),
    #Police Station
    path('reports/combined-metrics/', CombinedReportMetricsView.as_view(), name='combined-report-metrics'),
    path('reports/daily-count/', DailyReportCountView.as_view(), name='daily-report-count'),
    path('reports/needing-response/', ReportsNeedingResponseView.as_view(), name='reports-needing-response'),
    path('reports/resolved-count/', ResolvedReportsCountView.as_view(), name='resolved-reports-count'),
    path('reports/emergency-count/', EmergencyReportCountView.as_view(), name='emergency-report-count'),
    #Notification and Status update
    path('reports/<int:report_id>/update-status/', update_report_status, name='update-incident-status'),
    path('notifications/', views.get_user_notifications, name='get-notifications'),
    path('notifications/<int:notification_id>/mark-read/', views.mark_notification_as_read, name='mark-notification-read'),
]