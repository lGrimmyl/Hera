from django.contrib import admin
from .models import IncidentReport, Suspect, Victim, ChildConflict, IncidentCategory, IncidentSubcategory
# Register your models here.



class SuspectInline(admin.TabularInline):
    model = Suspect

class VictimInline(admin.TabularInline):
    model = Victim

class ChildConflictInline(admin.TabularInline):
    model = ChildConflict

class IncidentReportAdmin(admin.ModelAdmin):
    inlines = [SuspectInline, VictimInline, ChildConflictInline]

admin.site.register(IncidentCategory)

admin.site.register(IncidentSubcategory)

admin.site.register(IncidentReport, IncidentReportAdmin)