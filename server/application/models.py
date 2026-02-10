from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)
    user_id_primary = models.BigAutoField(primary_key=True)
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    pfp = models.URLField(blank=True, null=True)
    dob = models.DateField()

    def __str__(self):
        return self.user.username


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    taskID = models.CharField(max_length=36, primary_key=True)
    notes = models.TextField(blank=True, null=True)
    deadline = models.DateTimeField()
    remindAt = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title