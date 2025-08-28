from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id","recipient","actor","verb","timestamp","unread")
    list_filter = ("unread","verb","timestamp")

# Register your models here.
