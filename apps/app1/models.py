from __future__ import unicode_literals
from django.db import models
import re

class UserManager(models.Manager):
    def basic_validation(self,postData):
        error = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name'])<2:
            error["first_name"]="Enter more than character 2 for first name"
            
        if len(postData['last_name'])<2:
            error["last_name"]="Enter more than character 2 for last name"
        
        if postData['pass'] != postData['cpass'] :
            error["password"]="Password does not match"
        
        if len(postData['pass']) <8 :
            error["lowpassword"]="Password is less than 8 character"
            
        if not EMAIL_REGEX.match(postData['email']): 
            error["email"]="Enter a valid Email"
            
        return error


class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    
class Books(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    uploaded_by = models.ForeignKey(User,related_name = "books_uploaded")
    users_who_like = models.ManyToManyField(User,related_name='liked_books')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    