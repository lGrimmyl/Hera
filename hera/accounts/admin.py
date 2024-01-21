from django.contrib import admin
from .models import CustomUser
from .models import ValidIDType
admin.site.register(CustomUser)

# Register your models here.
@admin.register(ValidIDType)
class ValidIDTypeAdmin(admin.ModelAdmin):
    list_display = ['id_type']