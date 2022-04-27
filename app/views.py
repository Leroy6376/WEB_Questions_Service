from django.shortcuts import render


QUESTIONS = [
    {
        "title": f"Question #{i}",
        "text": f"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut placerat feugiat lacus et semper. Mauris gravida nibh eu malesuada accumsan. Donec sed lacinia metus. Nam maximus sodales posuere.",
        "tags": ["Lorem ipsum", "Techno Park", "Python"],
        "answers_count": "5",
        "id" : i
    } for i in range(1,5)
]
ANSWERS = [
    {
        "login": "Leroy",
        "text": f"Pellentesque luctus magna ultrices magna faucibus molestie. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Donec ac pulvinar nibh, eget congue nulla.",
        "likes": i,
    } for i in range(0,5)
]

TAGS = [
    {
        "id" : 0,
        "name" : "Perl",
        "button_type": "btn-outline-primary"
    },
    {
        "id" : 1,
        "name" : "Python",
        "button_type": "btn-outline-secondary"
    },
    {
        "id" : 2,
        "name" : "MySQL",
        "button_type": "btn-outline-success"
    },
    {
        "id" : 3,
        "name" : "Django",
        "button_type": "btn-outline-danger"
    },
    {
        "id" : 4,
        "name" : "C++",
        "button_type": "btn-outline-warning"
    },
    {
        "id" : 5,
        "name" : "GitHub",
        "button_type": "btn-outline-info"
    },
    {
        "id" : 6,
        "name" : "Techno Park",
        "button_type": "btn-outline-dark"
    }
]

PROFILE = {
    "id" : 1,
    "login" : "Leroy6376",
    "avatar" : "img/avatar.png",
    "nick" : "Leroy",
    "email" : "roza4466@mail.ru"
}
QUESTIONS_PAGES = {
        "previous" : -1,
        "current" : 0,
        "next" : 1,
        "max" : 5
    }

ANSWERS_PAGES = {
        "previous" : -1,
        "current" : 0,
        "next" : 1,
        "max" : 5
    }

# Create your views here.

def index(request):
    questions_paginator(0)
    return render(request, "index.html", {"questions" : QUESTIONS, "tags" : TAGS, "profile" : PROFILE, "page" : QUESTIONS_PAGES})

def question(request, i:int, page:int):
    ANSWERS = answer_paginator(page)
    if (4 * QUESTIONS_PAGES["current"]) == 0 :
        return render(request, "question.html", {"questions" : QUESTIONS[i - 1], "answers" : ANSWERS, "tags" : TAGS, "profile" : PROFILE,"page" : ANSWERS_PAGES})
    return render(request, "question.html", {"questions" : QUESTIONS[(i % (4 * QUESTIONS_PAGES["current"])) - 1], "answers" : ANSWERS, "tags" : TAGS, "profile" : PROFILE,"page" : ANSWERS_PAGES})

def ask(request):
    return render(request, "ask.html", {"tags" : TAGS, "profile" : PROFILE})

def tag(request, j:int, page:int):
    QUESTIONS = questions_paginator(page)
    return render(request, "tag.html", {"questions" : QUESTIONS, "interested_tag" : TAGS[j], "tags" : TAGS, "profile" : PROFILE, "page" : QUESTIONS_PAGES})

def profile(request, i:int):
    return render(request, "profile.html", {"tags" : TAGS, "profile" : PROFILE})

def log_out(request):
    PROFILE.clear()
    return index(request)

def log_in(request):
    return render(request, "log_in.html", {"tags" : TAGS})

def new_user(request):
    PROFILE["id"] = 1
    PROFILE["login"] = "Leroy6376"
    PROFILE["avatar"] = "img/avatar.png"
    PROFILE["nick"] = "Leroy"
    PROFILE["email"] = "roza4466@mail.ru"
    return index(request)

def register(request):
    return render(request, "register.html", {"tags" : TAGS})


def hot(request, page:int):
    QUESTIONS = questions_paginator(page)
    return render(request, "index.html", {"questions" : QUESTIONS, "tags" : TAGS, "profile" : PROFILE, "page" : QUESTIONS_PAGES})

def questions_paginator(page:int):
    QUESTIONS_PAGES["previous"] = page - 1
    QUESTIONS_PAGES["current"] = page
    QUESTIONS_PAGES["next"] = page + 1
    QUESTIONS.clear()
    temp_page = page * 4 + 1
    for i in range(temp_page, temp_page + 5):
        QUESTIONS.append({"title":f"Question #{i}", "text":f"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut placerat feugiat lacus et semper. Mauris gravida nibh eu malesuada accumsan. Donec sed lacinia metus. Nam maximus sodales posuere.", "tags":["Lorem ipsum", "Techno Park", "Python"], "answers_count":"5", "id":i })

    return QUESTIONS

def answer_paginator(page:int):
    ANSWERS_PAGES["previous"] = page - 1
    ANSWERS_PAGES["current"] = page
    ANSWERS_PAGES["next"] = page + 1
    ANSWERS.clear()
    temp_page = page * 4 + 1
    for i in range(temp_page, temp_page + 5):
        ANSWERS.append({"login":"Leroy", "text":f"Pellentesque luctus magna ultrices magna faucibus molestie. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Donec ac pulvinar nibh, eget congue nulla.", "likes":i })

    return ANSWERS