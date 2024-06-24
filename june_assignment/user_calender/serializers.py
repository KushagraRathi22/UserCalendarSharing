from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Calendar, Event, SharedCalendar


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        exclude = ['user']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_time', 'end_time', 'calendar', 'id']


class SharedCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedCalendar
        fields = ['id', 'calendar', 'shared_with', 'shared_by', 'shared_at']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"