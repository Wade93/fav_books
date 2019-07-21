from __future__ import unicode_literals
from django.db import models
import re
from datetime import *
import bcrypt

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        PW_REGEX = re.compile(r'^(?=.*[0-9]+.*)(?=.*[A-Z]+.*)[0-9a-zA-Z]{8,}$')
        if len(postData['fname']) < 1:
            errors['fname'] = "Please fill in the 'First Name' field."
        if len(postData['fname']) > 0:
            if len(postData['fname']) < 2:
                errors['fname'] = "First Name should be at least 2 characters."
        if len(postData['lname']) < 1:
            errors['lname'] = "Please fill in the 'Last Name' field."
        if len(postData['lname']) > 0:
            if len(postData['lname']) < 2:
                errors['lname'] = "Last Name should be at least 2 characters."
        if len(postData['email']) < 1:
            errors['email'] = "Please fill in the 'Email' field."
        if len(postData['email']) > 0:
            if not EMAIL_REGEX.match(postData['email']):
                errors['email'] = "Invalid email."
        check_email = User.objects.filter(email = postData['email'])
        if len(check_email) > 0:
            errors['email'] = "A user with that email address already exists."
        if len(postData['bdate']) < 1:
            errors['bdate'] = "Please fill in 'Date of Birth' field."
        if len(postData['bdate']) > 0:
            if datetime.strptime(postData['bdate'], '%Y-%m-%d') > datetime.today():
                errors['bdate'] = "Date must be in the past."
            # if (date(datetime.today())-date(datetime.strptime(postData['bdate'], '%Y-%m-%d'))).days < (13*365):
            #     errors['bdate'] = "Must be 13 years of age or older to register."
        if len(postData['password']) < 1:
            errors['password'] = "Please enter a password."
        if len(postData['password']) > 0:
            if not PW_REGEX.match(postData['password']):
                errors['password'] = "Passwords must be a minimum of 8 characters and include at least one Capital(s) and Number(0-9)"
        if postData['confirm_password'] != postData['password']:
            errors['confirm_password'] = "Passwords must match."
        return errors

    def log_in_validator(self, postData):
        errors = {}
        check_user = User.objects.filter(email = postData['email'])
        print("*"*50)
        print(check_user)
        print("*"*50)
        if len(check_user) == 0:
            errors['login'] = "Unable to log in."
        if len(check_user) > 0:
            pw_check = check_user[0].password.encode()
            if bcrypt.checkpw(postData['password'].encode(), pw_check):
                return errors
            else: errors['login'] = "Unable to log in."
        return errors

    def add_book_validator(self, postData):
        errors = {}
        if len(postData['title']) < 1:
            errors['title'] = "Please fill in the 'Title' field."
        if len(postData['description']) < 5:
            errors['description'] = "Descriptions should be at least 5 characters."
        return errors
        
class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    date_of_birth = models.DateField()
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

    def __repr__(self):
        return(f"Name: {self.first_name} {self.last_name}")

class Book(models.Model):
    title = models.CharField(max_length = 255)
    description = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name = "books_uploaded")
    favorited_by = models.ManyToManyField(User, related_name = "books_favorited")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

    def __repr__(self):
        return(f"Title: {self.title}")