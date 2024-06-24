# user_calender/tests.py

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Calendar, Event
from rest_framework_simplejwt.tokens import RefreshToken

class CalendarEventTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='Nikhil Kale', password='nikhil')
        self.calendar = Calendar.objects.create(user=self.user, description="Test Description")

        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_calendar(self):
        url = reverse('calendar-create')
        data = {
            "title": "Test Calendar",
            "description": "Calendar For Description"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Calendar.objects.count(), 2)
        self.assertEqual(Calendar.objects.get(id=response.data['id']).description, "Calendar For Description")

    def test_create_event(self):
        url = reverse('event-list-create')
        data = {
            "title": "Hiking Event",
            "description": "Hiking to Rishikesh",
            "start_time": "2024-06-25T09:00:00",
            "end_time": "2024-06-25T10:00:00",
            "calendar": self.calendar.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(Event.objects.get(id=response.data['id']).description, "Hiking to Rishikesh")

    def test_overlapping_event(self):
        Event.objects.create(
            title="Movie Event",
            description="Aavesham Movie Premier",
            start_time="2024-06-25T09:00:00",
            end_time="2024-06-25T10:00:00",
            calendar=self.calendar
        )

        url = reverse('event-list-create')
        data = {
            "title": "Overlapping Event",
            "description": "This event should overlap",
            "start_time": "2024-06-25T09:30:00",
            "end_time": "2024-06-25T10:30:00",
            "calendar": self.calendar.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "['Overlapping events are not allowed.']")
