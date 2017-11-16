from __future__ import unicode_literals
import re
from django.db import models
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Manager(models.Manager):
    def basicvalidator(self, postData, type):
        if type == "Register":
            errors = []
            if len(postData['fname']) < 0:
                errors.append("You need to enter in a first name!")
            if len(postData['lname']) < 0:
                errors.append("You need to enter in a last name!")
            if len(postData['password']) < 0:
                errors.append("You need to enter in a password!")
            if postData['confpw'] != postData['password']:
                errors.append("Your passwords do not match!")
            if len(postData['email']) < 0:
                errors.append("You need to enter in an email!")
            if not EMAIL_REGEX.match(postData['email']):
                errors.append("You need to enter in a valid email!")
            if len(errors) > 0:
                return errors
            elif len(errors) == 0:
                hashpass = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt(5))
                new_user = User.objects.create(fname=postData['fname'], lname=postData['lname'], email=postData['email'], password=hashpass)
                return new_user
        if type == "Login":
            lerrors = []
            if len(User.objects.filter(email=postData['Lemail'])) > 0:
                user = User.objects.filter(email=postData['Lemail'])[0]
                if not bcrypt.checkpw(postData['Lpassword'].encode(), user.password.encode()):
                    lerrors.append("Incorrect email or password")
                    return lerrors
            elif len(User.objects.filter(email=postData['Lemail'])) == 0:
                lerrors.append("Incorrect email or password")
                return lerrors
            return user


class User(models.Model):
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = Manager()

    def __str__(self):
        return User.objects.email()
