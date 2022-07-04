from pyexpat import model
from re import T
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill
import uuid

def upload_img_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['avatars', str(instance.userProfile.id)+str(instance.nickName)+str(".")+(ext)])

def upload_course_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['courses', str(instance.postUser.id)+str(instance.title)+str(".")+(ext)])

def upload_project_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['projects', str(instance.userProject.id)+str(instance.title)+str(".")+(ext)])

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
    
    username = models.CharField(max_length=50, unique=False, default='')
    email = models.EmailField(max_length=50, unique=True)
    last_login = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

class Profile(models.Model):
    
    class Meta:
        db_table = 'profile'

    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    nickName = models.CharField(max_length=20)
    userProfile = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name= 'userProfile',
        on_delete= models.CASCADE
    )
    selfIntro = models.CharField(max_length=100, default="")
    github_url = models.URLField(default="")
    created_at = models.DateField(auto_now_add=True)
    img = models.ImageField(blank=True, null=True, upload_to=upload_img_path)
    img_thumbnail = ImageSpecField(source='img', processors=[ResizeToFill(225, 225)],)

    def __str__(self):
        return self.nickName

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

class Project(models.Model):

    class Meta:
        db_table = 'project'
    
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=20)
    subtitle = models.CharField(max_length=50)
    language_category = models.CharField(max_length=50, default="")
    userProject = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name= 'project',
        on_delete= models.CASCADE
    )
    img = models.ImageField(
        blank=True, null=True, upload_to=upload_project_path,
    )
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name= 'liked', blank=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):

    class Meta:
        db_table = 'comment'

    text = models.CharField(max_length=100)
    userComment = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name= 'userComment',
        on_delete= models.CASCADE
    )
    post = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

