from __future__ import unicode_literals
from django.db import models
from ..login_reg.models import User

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

class Review(models.Model):
    text = models.TextField()
    rating = models.IntegerField(null=True)
    writer = models.ForeignKey(User, related_name="reviews")
    book = models.ForeignKey(Book, related_name="reviews")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
