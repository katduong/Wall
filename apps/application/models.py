from __future__ import unicode_literals
from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    # validator for registration form
    def basicValidatorReg(self, postData):
        errors = {}
        if len(postData['firstName']) < 1:
            errors['firstname'] = "This field is required"
        elif len(postData['firstName']) < 2:
            errors['firstname'] = "First name should be at least 2 characters"
        elif not postData['firstName'].isalpha():
            errors['firstname'] = "First name should contain only letters"
        if len(postData['lastName']) < 1:
            errors['lastname'] = "This field is required"
        elif len(postData['lastName']) < 2:
            errors['lastname'] = "Last name should be at least 2 characters"
        elif not postData['lastName'].isalpha():
            errors['lastname'] = "Last name should contain only letters"
        if len(postData['email']) < 1:
            errors['email'] = "This field is required"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address"
        # check if user with email exists in database
        else:
            user = User.objects.filter(email=postData['email'])
            if user:
                errors['email'] = "The email address you entered has already been taken."
        if len(postData['password']) < 1:
            errors['password'] = "This field is required"
        elif len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        if len(postData['password2']) < 1:
            errors['password2'] = "This field is required"
        elif postData['password'] != postData['password2']:
            errors['password2'] = "Passwords must match"

        return errors

    def basicValidatorLogin(self, postData):
        errors= {}
        if len(postData['email']) < 1:
            errors['emailLogin'] = "This field is required"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address" 
        if len(postData['password']) < 1:
            errors['passwordLogin'] = "This field is required"
        # check if user with email exists in database
        else:
            if len(postData['email']) > 1:
                user = User.objects.filter(email=postData['email'])
                if not user:
                    errors['emailLogin'] = "The email address you entered cannot be associated with a user"
                else:
                    if not bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
                        errors['passwordLogin'] = "Password incorrect. Please try again."
            else:
                errors['emailLogin'] = "This field is required"
        return errors


class User(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = UserManager()
