from django.db import models
from django.conf import settings

class Diagnose(models.Model):
    name = models.TextField(blank=False)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)


# class DiagnoseMember(models.Model):

#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diagnose_memberships', help_text='User ID') 
#     project = models.ForeignKey(Diagnose, on_delete=models.CASCADE, related_name='members', help_text='Diagnose ID')
#     enabled = models.BooleanField(default=True, help_text='Project member is enabled')
#     created_at = models.DateTimeField('created at', auto_now_add=True)
#     updated_at = models.DateTimeField('updated at', auto_now=True)