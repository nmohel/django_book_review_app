from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
    def register_validatior(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['name']) < 2:
            errors['name_length'] = "Name must be at least 2 characters"

        if len(postData['alias']) < 2:
            errors['alias'] = "Alias must be at least 2 characters"

        if not EMAIL_REGEX.match(postData['email']) or len(postData['email']) < 1 :
            errors['email_valid'] = "Not a valid email"
        elif User.objects.filter(email=postData['email']):
            errors['email_exists'] = "Someone with that email is already in the system. Login, or try a new email."

        if len(postData['password']) < 8:
            errors['password_len'] = "Password must be at least 8 characters"
        elif postData['password'] != postData['confirm_pw']:
            errors['password_match'] = "Password does not match confirm password"
        
        return errors

    def login_validator(self, postData):
        print postData
        errors = {}
        if len(postData['email']) < 1:
            errors['email_blank'] = "Please enter an email"
        elif len(postData['password']) < 1:
            errors['pw_blank'] = "Please enter a password"
        else:
            try:
                user = User.objects.get(email = postData['email'])
            except:
                errors['no_email'] = "Cannot find a user with that email"
            else:
                try_pw = postData['password']
                if not bcrypt.checkpw(try_pw.encode(), user.password.encode()):
                    errors['wrong_pw'] = "Incorrect password"
        
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=255)

    objects = UserManager()
