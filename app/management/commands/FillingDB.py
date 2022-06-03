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
        TAGS = TAGS[::3]
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
        answers_count = models.Answer.objects.count()
        answer_model_type = ContentType.objects.get_for_model(ANSWERS_TO_CREATE[0])
        
        Likes_TO_CREATE = []
        j = 0
        k = 0
        for i in range(0, 200):
            if j == answers_count - 1:
                j = 0

            if k == profiles_count:
                k = 0

            Likes_TO_CREATE.append(models.Like(content_type=answer_model_type, object_id=answers[j].id, author=profiles[k]))
            i += 1
            j += 1
            k += 1

        models.Like.objects.bulk_create(Likes_TO_CREATE)
        print("Likes added successfully")

        #Создание и загрузка вопросов
        questions_file = "static/questions.txt"
        QUESTIONS = open(questions_file).read().splitlines()
        QUESTIONS = QUESTIONS[::2]

        tags = models.Tag.objects.get_queryset()
        temp_answer = 0
        QUESTIONS_TO_CREATE = []
        k = 0
        g = 0
        p = 0
        questions_count = len(QUESTIONS)
        for i in range(0, 110000):
            tags_count = random.randint(1, 10)
            TAG = []
            for j in range(0, tags_count):
                TAG.append(tags[random.randint(0, models.Tag.objects.count())])
            
            answer = []
            for j in range(temp_answer, temp_answer + 11):
                answer.append(answers[j])
            temp_answer += 11

            if k == answers_count - 1:
                k = 0

            if g == questions_count:
                g = 0

            if p == profiles_count:
                p = 0
            
            QUESTION = models.Question(header=ANSWERS[k], body=QUESTIONS[g], author=profiles[p])
            tag = models.Tag.objects.get_queryset()
            QUESTION.tags.add(tag[0].id)
            QUESTIONS_TO_CREATE.append(QUESTION)
            k += 1
            g += 1
            p += 1

        models.Question.objects.bulk_create(QUESTIONS_TO_CREATE)
        print("Question added successfully")
        print("Database populated successfully")

