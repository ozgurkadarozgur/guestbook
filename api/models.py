from django.db import models


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Entry(models.Model):
    id = models.BigAutoField(primary_key=True)
    subject = models.CharField(max_length=100, null=False)
    message = models.CharField(max_length=100, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
