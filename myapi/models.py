from django.contrib.auth.models import User
from django.db import models

class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)


class Detail(models.Model):
    department = models.CharField(max_length=100)
    year = models.CharField(max_length=4)
    subject = models.CharField(max_length=100)

class Meta:
    unique_together = ('department', 'year', 'subject')

    def __str__(self):
        return f"{self.department} - {self.year} - {self.subject}"
class Questions(models.Model):
    Qdepartment = models.CharField(max_length=100)
    Qyear = models.CharField(max_length=4)
    Qsubject = models.CharField(max_length=100)
    Qquestion = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    marks = models.IntegerField()
    used = models.BooleanField(default=False)