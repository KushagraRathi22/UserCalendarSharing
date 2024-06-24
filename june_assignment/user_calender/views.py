from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from .models import Event, Calendar, SharedCalendar
from .serializers import EventSerializer, CalendarSerializer, SharedCalendarSerializer, UserSerializer
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User





class CalendarCreateView(generics.CreateAPIView):

    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]  

    def perform_create(self, serializer):
        
        serializer.save(user=self.request.user)

class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]  
    authentication_classes = [JWTAuthentication]  

    def perform_create(self, serializer):
        # print("serializer",serializer)
        start_time = serializer.validated_data['start_time']
        end_time = serializer.validated_data['end_time']
        calendar = serializer.validated_data['calendar']
        # print("calendar_id",calendar)
        overlapping_events = Event.objects.filter(
            calendar=calendar,
            start_time__lt=end_time,
            end_time__gt=start_time
        )
        if overlapping_events.exists():
            raise ValidationError("Overlapping events are not allowed.")
        serializer.save()
    
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class EventRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]  
    authentication_classes = [JWTAuthentication]  

    def perform_update(self, serializer):
       
        instance = serializer.instance
        start_time = serializer.validated_data.get('start_time', instance.start_time)
        end_time = serializer.validated_data.get('end_time', instance.end_time)
        calendar = serializer.validated_data.get('calendar_id', instance.calendar)
        overlapping_events = Event.objects.filter(
            calendar_id=calendar,
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exclude(pk=instance.pk)
        if overlapping_events.exists():
            raise ValidationError("Overlapping events are not allowed.")
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


class ShareCalendarView(generics.CreateAPIView):
    queryset = SharedCalendar.objects.all()
    serializer_class = SharedCalendarSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        calendar_id = request.data.get('calendar_id')
        shared_with_id = request.data.get('shared_with_id')
        
        try:
            calendar = Calendar.objects.get(id=calendar_id)
            shared_with = User.objects.get(id=shared_with_id)

        except Calendar.DoesNotExist:
            return Response({"detail": "Calendar not found."}, status=status.HTTP_404_NOT_FOUND)
        
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

      


        if request.user != calendar.user:
            return Response({"detail": "You do not have permission to share this calendar."},
                            status=status.HTTP_403_FORBIDDEN)
        
        shared_calendar, created = SharedCalendar.objects.get_or_create(
            calendar=calendar,
            shared_with=shared_with,
            shared_by=request.user
        )

        if created:
            return Response({"detail": "Calendar shared successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Calendar is already shared with this user."}, status=status.HTTP_200_OK)

class ListSharedCalendarsView(generics.ListAPIView):
    serializer_class = SharedCalendarSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    

    def get_queryset(self):
        queryset = SharedCalendar.objects.filter(shared_by=self.request.user)
        serialized_data = self.serializer_class(queryset, many=True).data
        print(serialized_data)  
        return queryset


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    