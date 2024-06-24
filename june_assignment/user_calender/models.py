from django.db import models
from django.contrib.auth.models import User

class Calendar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=255, blank=True, null=True, default="")
    shared_with = models.ManyToManyField(User, related_name='shared_to_users', blank=True)

    def __str__(self):
        return self.description


class Event(models.Model):
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True, default="")
    description = models.TextField(max_length=255, blank=True, null=True, default="")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.title


class SharedCalendar(models.Model):
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_calendars')
    shared_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_by')
    shared_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('calendar', 'shared_with')