from contextlib import nullcontext
import json
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import auth 
from app.forms import AnswerForm, LoginForm, ProfileForm, QuestionForm, RegistrationForm
from . import models
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    return new_question(request, 0)

def question(request, i:int, page:int):
    QUESTION = models.Question.objects.get(pk=i)
    TAGS = models.TagManager.GetHotTags(9)
    ANSWERS = models.QuestionManager.GetAnswers(QUESTION)
    p = Paginator(ANSWERS, 4)
    ANSWERS = p.page(page + 1)
    PAGES = get_page_struct(page, p.num_pages)
    
    if request.method == "GET":
        if request.user:
            form = AnswerForm()
        else:
            form = AnswerForm(disabled=True)
    elif request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            form.save(QUESTION, request.user.profile)
            ANSWERS = models.QuestionManager.GetAnswers(QUESTION)
            p = Paginator(ANSWERS, 4)
            return redirect(reverse("question_url", args=[i, p.num_pages - 1]))

    return render(request, "question.html", {"question" : QUESTION, "answers" : ANSWERS, "tags" : TAGS, "page" : PAGES, "form" :form})

def ask(request):
    TAGS = models.TagManager.GetHotTags(9)

    if request.method == "GET":
        form = QuestionForm()
    elif request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(request.user.profile)     
            return redirect(reverse("question_url", args=[question.id, 0]))

    return render(request, "ask.html", {"tags" : TAGS, "form" : form})


def profile(request, i:int):
    TAGS = models.TagManager.GetHotTags(9)

    if request.method == "GET":
        initial_data = model_to_dict(request.user)
        initial_data['avatar'] = request.user.profile.avatar
        form = ProfileForm(initial=initial_data)
    elif request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse("profile_url", args=[request.user.profile]))

    return render(request, "profile.html", {"tags" : TAGS, "form" : form})

def log_out(request):
    auth.logout(request)
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
            user = form.save()
            auth.login(request, user)
            return redirect(reverse("home"))
    
    return render(request, "register.html", {"tags" : TAGS, "form" : form})


def tag(request, j:int, page:int):
    QUESTION = models.QuestionManager.GetQuestionByTag(j)
    Tag = models.Tag.objects.get(id=j)
    p = Paginator(QUESTION, 5)
    QUESTION = p.page(page + 1)
    PAGES = get_page_struct(page, p.num_pages)
    TAGS = models.TagManager.GetHotTags(9)
    return render(request, "tag.html", {"questions" : QUESTION, "tags" : TAGS, "page" : PAGES, "id" : j, "name" : Tag.name})

def hot(request, page:int):
    QUESTION = models.QuestionManager.GetHotQuestions()
    return question_list(request, page, QUESTION, "Popular questions", "hot")

def new_question(request, page:int):
    QUESTION = models.QuestionManager.GetNewQuestions()
    return question_list(request, page, QUESTION, "New questions", "new")

def get_page_struct(page:int, max:int):
    Page_struct = {}
    Page_struct["previous"] = page - 1
    Page_struct["current"] = page
    Page_struct["next"] = page + 1
    Page_struct["max"] = max - 1
    return Page_struct

def question_list(request, page, QUESTION, TEXT, LINK):
    p = Paginator(QUESTION, 5)
    QUESTION = p.page(page + 1)
    PAGES = get_page_struct(page, p.num_pages)
    TAGS = models.TagManager.GetHotTags(9)
    return render(request, "index.html", {"questions" : QUESTION, "tags" : TAGS, "page" : PAGES, "text" : TEXT, "link" : LINK})


def question_vote(request):
    question_id = request.POST['question_id']
    question = models.Question.objects.get(pk=question_id)
    if not models.LikeManager.is_fan(question, request.user.profile):
        models.LikeManager.add_like(question, request.user.profile)
    else:
        models.LikeManager.remove_like(question, request.user.profile)

    new_rating = question.likes.count()
    return JsonResponse({'new_rating' : new_rating})

def answer_vote(request):
    print(request.POST)
    answer_id = request.POST['answer_id']
    answer = models.Answer.objects.get(pk=answer_id)
    if not models.LikeManager.is_fan(answer, request.user.profile):
        models.LikeManager.add_like(answer, request.user.profile)
    else:
        models.LikeManager.remove_like(answer, request.user.profile)

    new_rating = answer.likes.count()
    return JsonResponse({'new_rating' : new_rating})

def checkbox_vote(request):
    print(request.POST)
    answer_id = request.POST['answer_id']
    question_id = request.POST['question_id']
    value = request.POST['value']
    
    answer = models.AnswerManager.change_correct(answer_id, value)
    return JsonResponse({'value' : answer.is_correct})