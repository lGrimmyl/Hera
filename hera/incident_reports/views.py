from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView
from .models import IncidentReport

class ReportListView(ListView):
    model = IncidentReport
    template_name = 'incident_reports/report_list.html'

class ReportCreateView(CreateView):
    model = IncidentReport
    fields = [ 'photo', 'description', 'narrative']
    template_name = 'incident_reports/report_form.html'

class ReportDetailView(DetailView):
    model = IncidentReport
    template_name = 'incident_reports/report_detail.html'