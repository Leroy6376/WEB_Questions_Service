from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import auth 
from app.forms import LoginForm
from . import models
from django.core.paginator import Paginator

PROFILE = {}


# Create your views here.

def index(request):
    return new_question(request, 0)

def question(request, i:int, page:int):
    QUESTION = models.Question.objects.get(pk=i)

    ANSWERS = models.QuestionManager.GetAnswers(QUESTION)
    p = Paginator(ANSWERS, 4)
    ANSWERS = p.page(page + 1)
    PAGES = get_page_struct(page, p.num_pages)
    TAGS = models.TagManager.GetHotTags(9)
    if request.user.is_authenticated:
        PROFILE = models.Profile.objects.get(pk=request.user.id)
    
    return render(request, "question.html", {"question" : QUESTION, "answers" : ANSWERS, "tags" : TAGS, "profile" : PROFILE, "page" : PAGES})

def ask(request):
    TAGS = models.TagManager.GetHotTags(9)
    if request.user.is_authenticated:
        PROFILE = models.Profile.objects.get(pk=request.user.id)
    return render(request, "ask.html", {"tags" : TAGS, "profile" : PROFILE})


def profile(request, i:int):
    TAGS = models.TagManager.GetHotTags(9)
    return render(request, "profile.html", {"tags" : TAGS, "profile" : PROFILE})

def log_out(request):
    auth.logout(request)
    return index(request)

def log_in(request):
    TAGS = models.TagManager.GetHotTags(9)
    if request.method == "GET":
        form = LoginForm()
    elif request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user:
                auth.login(request, user)
                print(request.user.is_authenticated)
                profile = models.Profile.objects.get(pk=request.user.id)
                print(profile.avatar)
                return redirect(reverse("home"))
    
    return render(request, "login.html", {"tags" : TAGS, "form" : form})

def new_user(request):
    PROFILE["id"] = 1
    PROFILE["login"] = "Leroy6376"
    PROFILE["avatar"] = "img/avatar.png"
    PROFILE["nick"] = "Leroy"
    PROFILE["email"] = "roza4466@mail.ru"
    return index(request)

def register(request):
    TAGS = models.TagManager.GetHotTags(9)
    return render(request, "register.html", {"tags" : TAGS})


def tag(request, j:int, page:int):
    QUESTION = models.QuestionManager.GetQuestionByTag(j)
    Tag = models.Tag.objects.get(id=j)
    p = Paginator(QUESTION, 5)
    QUESTION = p.page(page + 1)
    PAGES = get_page_struct(page, p.num_pages)
    TAGS = models.TagManager.GetHotTags(9)
    if request.user.is_authenticated:
        PROFILE = models.Profile.objects.get(pk=request.user.id)
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
    if request.user.is_authenticated:
        PROFILE = models.Profile.objects.get(pk=request.user.id)
    return render(request, "index.html", {"questions" : QUESTION, "tags" : TAGS, "profile" : PROFILE, "page" : PAGES, "text" : TEXT, "link" : LINK})
