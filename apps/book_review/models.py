from __future__ import unicode_literals
from django.db import models
from ..login_reg.models import User

class BookManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['title']) < 1:
            errors['title_len'] = "Title cannot be blank"
        elif Book.objects.filter(title=postData['title']):
            errors['title_exist'] = postData['title'] + " is already on the site! Please add your review to existing book."
        
        if len(postData['author_new']) < 1:
            if 'author_list' not in postData:
                errors['no_author'] = "Please choose an author or add your own."

        if len(postData['review_text']) < 1 :
            errors['review_len'] = "Review cannot be blank"
        
        return errors

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = BookManager()

class ReviewManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['review_text']) < 1 :
            errors['review_len'] = "Review cannot be blank"
        return errors

class Review(models.Model):
    text = models.TextField()
    rating = models.IntegerField(null=True)
    writer = models.ForeignKey(User, related_name="reviews")
    book = models.ForeignKey(Book, related_name="reviews")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ReviewManager()
