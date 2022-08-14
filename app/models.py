from cProfile import label
from email.policy import default
from unittest import defaultTestLoader
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill
import uuid
from django.utils import timezone

def upload_img_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['avatars', str(instance.id)+str(instance.email)+str(".")+(ext)])

def upload_course_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['courses', str(instance.postUser.id)+str(instance.title)+str(".")+(ext)])

def upload_project_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['plans', str(instance.userPlan.id)+str(instance.title)+str(".")+(ext)])

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Email is must')
        
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):

    class Meta:
        db_table = 'user'
    
    username = models.CharField(max_length=50, unique=False, default='',)
    email = models.EmailField(max_length=50, unique=True)
    img = models.ImageField(blank=True, null=True, default="", upload_to=upload_img_path)
    img_thumbnail = ImageSpecField(
        source='img', 
        processors=[ResizeToFill(225, 225)],
        format="png",
        options={"quality": 80}
    )
    selfIntro = models.CharField(max_length=100, default="", blank=True)
    github_url = models.URLField(default="", blank=True)
    last_login = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

class Course(models.Model):

    class Meta:
        db_table = 'course'

    title = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    img = models.ImageField(upload_to=upload_course_path)
    learning_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name= 'learning_user')
    postUser = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name= 'postUser',
        on_delete= models.CASCADE, default= 0, 
    )
    content = models.URLField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

class Plan(models.Model):

    class Meta:
        db_table = 'plan'
    
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=500)
    language_category = models.CharField(max_length=100, default="")
    userPlan = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name= 'plan',
        on_delete= models.CASCADE
    )
    img = models.ImageField(
        blank=True, null=True, upload_to=upload_project_path,
    )
    img_thumbnail = ImageSpecField(
        source='img',
        processors=[ResizeToFill(670, 370)],
        format="png",
        options={"quality": 80}
    )
    repository_url = models.URLField(default="", null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):

    class Meta:
        db_table = 'comment'

    text = models.TextField(max_length=100, default='')
    userComment = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name= 'userComment',
        on_delete= models.CASCADE
    )
    post = models.ForeignKey(Plan, on_delete=models.CASCADE)
    create_at = models.DateTimeField()

    def __str__(self):
        return self.text