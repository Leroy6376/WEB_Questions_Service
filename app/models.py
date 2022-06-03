from ctypes.wintypes import tagSIZE
from email.policy import default
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

# Create your models here.

class TagManager(models.Manager):
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=128)
    views = models.PositiveIntegerField(default=0)

    objects = TagManager

    def __str__(self):
        return self.name

class ProfileManager(models.Manager):
    def __str__(self):
        return self.user.username

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(default="static/img/avatar.png")

    objects = ProfileManager

    def __str__(self):
        return self.user.username


class Like(models.Model):
    author = models.ForeignKey(Profile, related_name='likes', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

class AnswerManager(models.Manager):
    def __str__(self):
        return 

class Answer(models.Model):
    body = models.TextField()
    likes = GenericRelation(Like)
    creation_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)

    objects = AnswerManager



class QuestionManager(models.Manager):
    def __str__(self):
        return self.header

class Question(models.Model):
    header = models.CharField(max_length=128)
    body = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField()
    avatar = models.ImageField(default="static/img/56854.png")
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    answers = models.ManyToManyField(Answer, blank=True)

    objects = QuestionManager

    def __str__(self):
        return self.header