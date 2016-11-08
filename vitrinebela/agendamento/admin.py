from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CalendarEvent


admin.site.register(CalendarEvent)