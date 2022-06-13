from contextlib import nullcontext
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import auth 
from app.forms import AnswerForm, LoginForm, ProfileForm, QuestionForm, RegistrationForm
from . import models
from django.core.paginator import Paginator
from django.contrib.auth.models import User

PROFILE = {}


# Create your views here.

def index(request):
    return new_question(request, 0)

def question(request, i:int, page:int):
    QUESTION = models.Question.objects.get(pk=i)
    TAGS = models.TagManager.GetHotTags(9)
    PROFILE = profile_check(request)
    ANSWERS = models.QuestionManager.GetAnswers(QUESTION)
    p = Paginator(ANSWERS, 4)
    ANSWERS = p.page(page + 1)
    PAGES = get_page_struct(page, p.num_pages)
    
    if request.method == "GET":
        if PROFILE:
            form = AnswerForm()
        else:
            form = AnswerForm(disabled=True)
    elif request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = models.Answer.objects.create(body=form.cleaned_data['body'], author=PROFILE)
            QUESTION.answers.add(answer)
            ANSWERS = models.QuestionManager.GetAnswers(QUESTION)
            p = Paginator(ANSWERS, 4)
            return redirect(reverse("question_url", args=[i, p.num_pages - 1]))

    return render(request, "question.html", {"question" : QUESTION, "answers" : ANSWERS, "tags" : TAGS, "profile" : PROFILE, "page" : PAGES, "form" :form})

def ask(request):
    TAGS = models.TagManager.GetHotTags(9)
    PROFILE = profile_check(request)

    if request.method == "GET":
        form = QuestionForm()
    elif request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            Question = models.Question.objects.filter(header=form.cleaned_data['header'], body=form.cleaned_data['body']).order_by("-creation_date")
            if form.cleaned_data["new_tag"] != nullcontext:
                New_tags = form.cleaned_data["new_tag"].split()
                for tag in New_tags:
                    tag = models.Tag.objects.create(name=tag)
                    Question[0].tags.add(tag.id)
                   
            return redirect(reverse("question_url", args=[Question[0].id, 0]))

    return render(request, "ask.html", {"tags" : TAGS, "profile" : PROFILE, "form" : form})


def profile(request, i:int):
    TAGS = models.TagManager.GetHotTags(9)
    PROFILE = profile_check(request)

    if request.method == "GET":
        form = ProfileForm(instance=PROFILE.user)
    elif request.method == "POST":
        form = ProfileForm(data=request.POST, instance=PROFILE.user)
        if form.is_valid():
            #Обработка новой аватарки от пользователя
            form.save()
    return render(request, "profile.html", {"tags" : TAGS, "profile" : PROFILE, "form" : form})

def log_out(request):
    auth.logout(request)
    PROFILE.clear()
    return redirect(reverse("home"))

def log_in(request):
    TAGS = models.TagManager.GetHotTags(9)

    if request.method == "GET":
        form = LoginForm()
    elif request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            auth.login(request, auth.authenticate(request, **form.cleaned_data))
            return redirect(reverse("home"))
    
    return render(request, "login.html", {"tags" : TAGS, "form" : form})


def register(request):
    TAGS = models.TagManager.GetHotTags(9)

    if request.method == "GET":
        form = RegistrationForm()
    elif request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # сохранение аватарки пользователя
            form.save()
            user = User.objects.get_queryset().filter(username=form.cleaned_data['username'])
            models.Profile.objects.create(user=user[0], avatar=form.cleaned_data['avatar'])
            auth.login(request, user[0])
            return redirect(reverse("home"))
    
    return render(request, "register.html", {"tags" : TAGS, "form" : form})


def tag(request, j:int, page:int):
    QUESTION = models.QuestionManager.GetQuestionByTag(j)
    Tag = models.Tag.objects.get(id=j)
    p = Paginator(QUESTION, 5)
    QUESTION = p.page(page + 1)
    PAGES = get_page_struct(page, p.num_pages)
    TAGS = models.TagManager.GetHotTags(9)
    PROFILE = profile_check(request)
    return render(request, "tag.html", {"questions" : QUESTION, "tags" : TAGS, "profile" : PROFILE, "page" : PAGES, "id" : j, "name" : Tag.name})

def hot(request, page:int):
    QUESTION = models.QuestionManager.GetHotQuestions()
    return question_list(request, page, QUESTION, PROFILE, "Popular questions", "hot")

def new_question(request, page:int):
    QUESTION = models.QuestionManager.GetNewQuestions()
    return question_list(request, page, QUESTION, PROFILE, "New questions", "new")

def get_page_struct(page:int, max:int):
    Page_struct = {}
    Page_struct["previous"] = page - 1
    Page_struct["current"] = page
    Page_struct["next"] = page + 1
    Page_struct["max"] = max - 1
    return Page_struct

def question_list(request, page, QUESTION, PROFILE, TEXT, LINK):
    p = Paginator(QUESTION, 5)
    QUESTION = p.page(page + 1)
    PAGES = get_page_struct(page, p.num_pages)
    TAGS = models.TagManager.GetHotTags(9)
    PROFILE = profile_check(request)
    return render(request, "index.html", {"questions" : QUESTION, "tags" : TAGS, "profile" : PROFILE, "page" : PAGES, "text" : TEXT, "link" : LINK})


def profile_check(request):
    if request.user.is_authenticated:
        PROFILE = models.Profile.objects.get(user_id=request.user.id)
    else:
        PROFILE = {}
    return PROFILE
