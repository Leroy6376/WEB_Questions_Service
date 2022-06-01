from django.core.management.base import BaseCommand
import requests
from app import models
from django.contrib.auth.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):

        #tags_file = "static/tags.txt"
        #TAGS = open(tags_file).read().splitlines()
        #TAGS = TAGS[::3]
        #TAGS_TO_CREATE = [models.Tag(name=i) for i in TAGS if len(i) > 3]
        #models.Tag.objects.bulk_create(TAGS_TO_CREATE)

        names_file = "static/names.txt"
        USER_NAMES = open(names_file).read().splitlines()
        PROFILE_TO_CREATE = [models.Profile(user=User.objects.create(username=Name.decode('utf-8'))) for Name in set(USER_NAMES)]
        #models.Profile.objects.bulk_create(PROFILE_TO_CREATE)

        #for i in range(0, 10):
            #print(USER_NAMES[i].decode('utf-8'))
            #models.Answer.objects.bulk_create()