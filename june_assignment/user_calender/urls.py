from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.CalendarCreateView.as_view(), name='calendar-create'),
    path('events/', views.EventListCreateView.as_view(), name='event-list-create'),
    path('events/<int:pk>/', views.EventRetrieveUpdateDestroyView.as_view(), name='event-detail'),
    path('share/', views.ShareCalendarView.as_view(), name='calendar-share'),
    path('shared/', views.ListSharedCalendarsView.as_view(), name='shared-calendars'),
    path('users/', views.UserListView.as_view(), name='user-list'),
]
