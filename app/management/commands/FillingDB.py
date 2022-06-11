import requests
from app import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
import random


class Command(BaseCommand):

    def handle(self, *args, **options):
        
        #Создание и загрузка тегов
        tags_file = "static/tags.txt"
        TAGS = open(tags_file).read().splitlines()
        TAGS = TAGS[::2]
        TAGS_TO_CREATE = [models.Tag(name=i) for i in TAGS if len(i) > 3]
        models.Tag.objects.bulk_create(TAGS_TO_CREATE)
        print("Tags added successfully")

        #Создание и загрузка user и профелей пользователей
        names_file = "static/names.txt"
        USER_NAMES = open(names_file).read().splitlines()
        PROFILE_TO_CREATE = [models.Profile(user=User.objects.create(username=Name)) for Name in set(USER_NAMES)]
        models.Profile.objects.bulk_create(PROFILE_TO_CREATE)
        print("Profiles added successfully")

        #Создание и загрузка ответов
        answers_file = "static/answers.txt"
        ANSWERS = open(answers_file).read().splitlines()

        answers_count = len(ANSWERS)
        j = 0
        profiles_count = len(PROFILE_TO_CREATE)
        k = 0
        ANSWERS_TO_CREATE = []

        for i in range(0, 1001000):
            if j == answers_count:
                j = 0

            if k == profiles_count:
                k = 0

            ANSWERS_TO_CREATE.append(models.Answer(body=ANSWERS[j], author=PROFILE_TO_CREATE[k]))
            i+=1
            j+=1
            k+=1

        models.Answer.objects.bulk_create(ANSWERS_TO_CREATE)
        print("Answers added successfully")

        #Создание и загрузка лайков для ответов
        answers = models.Answer.objects.get_queryset()
        profiles = models.Profile.objects.get_queryset()
        profiles_count = models.Profile.objects.count()
        answer_model_type = ContentType.objects.get_for_model(answers[0])
        
        Likes_TO_CREATE = [models.Like(content_type=answer_model_type, object_id=answer.id, author=profiles[random.randint(0, profiles_count - 1)]) for k in range(0,2) for answer in answers]
        models.Like.objects.bulk_create(Likes_TO_CREATE)
        print("Likes added successfully")

        #Создание и загрузка вопросов
        questions_file = "static/questions.txt"
        QUESTIONS = open(questions_file).read().splitlines()
        QUESTIONS = QUESTIONS[::2]

        questions_count = len(QUESTIONS)
        answers_count = models.Answer.objects.count()
        ANSWERS = models.Answer.objects.get_queryset()
        profiles_count = models.Profile.objects.count()

        QUESTIONS_TO_CREATE = [models.Question(header=ANSWERS[random.randint(0, answers_count - 1)].body, body=QUESTIONS[random.randint(0, questions_count - 1)], author=profiles[random.randint(0, profiles_count - 1)]) for i in range(0, 110000)]
        models.Question.objects.bulk_create(QUESTIONS_TO_CREATE)

        answer = models.Answer.objects.get_queryset()
        tag = models.Tag.objects.get_queryset()
        QUESTIONs = models.Question.objects.get_queryset()
        for QUESTION in QUESTIONs:
            tags_count = random.randint(1, 10)
            tags_start = random.randint(0, tag.count() - 10)
            QUESTION.tags.set(tag[tags_start : tags_start + tags_count])

            answers_count = random.randint(1, 10)
            answers_start = random.randint(0, answer.count() - 10)
            QUESTION.answers.set(answer[answers_start : answers_start + answers_count])
  
        print("Question added successfully")
        print("Database populated successfully")

