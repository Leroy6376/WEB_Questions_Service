from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

# Create your models here.

class TagManager(models.Manager):
    def GetHotTags(count):
        HOT_TAGS = Tag.objects.get_queryset().order_by("-views")
        return HOT_TAGS[:count]

    def UpdateViews(id):
        TAG = Tag.objects.get(pk=id)
        TAG.views += 1
        TAG.save()
        return

    

class Tag(models.Model):
    name = models.CharField(max_length=128)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    objects = TagManager


class ProfileManager(models.Manager):
    def __str__(self):
        return self.user.username

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(default="static/img/avatar.png", upload_to='static/img/')

    def __str__(self):
        return self.user.username

    objects = ProfileManager

class LikeManager(models.Manager):
    def add_like(obj, user):
        obj_type = ContentType.objects.get_for_model(obj)
        like, is_created = Like.objects.get_or_create(content_type=obj_type, object_id=obj.id, author=user)
        return like

    def remove_like(obj, user):
        obj_type = ContentType.objects.get_for_model(obj)
        Like.objects.filter(content_type=obj_type, object_id=obj.id, author=user).delete()

    def is_fan(obj, user) -> bool:
        if not user.user.is_authenticated:
            return False
        obj_type = ContentType.objects.get_for_model(obj)
        likes = Like.objects.filter(content_type=obj_type, object_id=obj.id, author=user)
        return likes.exists()

    def get_fans(obj):
        obj_type = ContentType.objects.get_for_model(obj)
        return Profile.objects.filter(likes__content_type=obj_type, likes__object_id=obj.id)


class Like(models.Model):
    author = models.ForeignKey(Profile, related_name='likes', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = LikeManager

class AnswerManager(models.Manager):
    def __str__(self):
        return self.author.user.username + " : " + self.body 

class Answer(models.Model):
    body = models.TextField()
    likes = GenericRelation(Like)
    creation_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.author.user.username + " : " + self.body

    objects = AnswerManager




class QuestionManager(models.Manager):
    def GetNewQuestions():
        return Question.objects.get_queryset().order_by("-creation_date")

    def GetHotQuestions():
        return Question.objects.get_queryset().order_by("-views")

    def GetQuestionByTag(id):
        TagManager.UpdateViews(id)
        return Question.objects.get_queryset().filter(tags__id=id)

    def UpdateViews(self):
        self.views += 1
        self.save()
        return

    def GetAnswers(self):
        QuestionManager.UpdateViews(self)
        for tag in self.tags.get_queryset():
            TagManager.UpdateViews(tag.id)
        return self.answers.get_queryset()

class Question(models.Model):
    header = models.CharField(max_length=128)
    body = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    avatar = models.ImageField(default="static/img/56854.png", upload_to='static/img/')
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    answers = models.ManyToManyField(Answer, blank=True)

    def __str__(self):
        return self.header

    objects = QuestionManager
