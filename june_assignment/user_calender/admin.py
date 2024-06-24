from django.contrib import admin
from .models import Calendar, Event, SharedCalendar
# Register your models here.
admin.site.register(Calendar)
admin.site.register(Event)
admin.site.register(SharedCalendar)