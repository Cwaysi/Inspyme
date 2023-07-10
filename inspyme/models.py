from django.contrib.auth.models import AbstractUser, User
from django.db import models
from datetime import date, datetime
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager


# user manager
class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = CustomUser(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        assert extra_fields["is_staff"]
        assert extra_fields["is_superuser"]
        return self._create_user(email, password, **extra_fields)


#user account
class CustomUser(AbstractUser):
    GENDER = [("M", "Male"), ("F", "Female")]

    username = models.CharField(max_length=30, null=True, blank=True)  # Removed username, using email instead
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=1, choices=GENDER)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email" #make email the user entry field
    REQUIRED_FIELDS = []
    object = CustomUserManager() #call the user manager to save user
    def __str__(self):
        #string representation of the user model, lastname and firstname
        return self.last_name + ", " + self.first_name

#Chat model for the help aspect
# class Chat(models.Model):
#     sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_chats')
#     recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_chats')
#     timestamp = models.DateTimeField(auto_now_add=True)
#     message = models.TextField()
   
    
#Class model to save all stories
class Story(models.Model):
    author = models.ForeignKey(CustomUser, null=True, blank = False, on_delete=models.CASCADE) #the one posting the story
    tag = models.CharField(max_length=100, null=True, blank=False) #give the story a title or a tag 
    story = models.TextField(null=True, blank=False) #the actual story
    is_anonymous = models.BooleanField(default=True) #user should choose to show identity or not
    date_posted = models.DateTimeField (auto_now=True) #picks current date and time
    
    def __str__(self):
        #string representation of the model, the tag, author name and date
        return str(self.tag) + " " + str(self.author.first_name) + " " + str(self.date_posted)

#Class to save comments
class Comment(models.Model):
    author = models.ForeignKey(CustomUser, null=True, blank = False, on_delete=models.CASCADE) #the one posting the comment
    story = models.ForeignKey(Story, null=True, blank = False, on_delete=models.CASCADE) #the story being commented on
    comment = models.TextField(null=True, blank=False) #the comment to the story
    is_anonymous = models.BooleanField(default=True) #user should choose to show identity or not
    date_posted = models.DateTimeField (auto_now=True) #picks current date and time
    
    def __str__(self):
        #string representation of the model, the tag, author name and date
        return str(self.story.tag) + " " + str(self.author.first_name) + " " + str(self.date_posted)
    
