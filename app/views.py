from django.shortcuts import render

QUESTIONS = [
    {
        "title": f"Question #{i}",
        "text": f"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut placerat feugiat lacus et semper. Mauris gravida nibh eu malesuada accumsan. Donec sed lacinia metus. Nam maximus sodales posuere.",
        "tags": ["Lorem ipsum", "Techno Park", "Python"],
        "answers_count": "5",
        "id" : i,
    } for i in range(1,5)
]

# Create your views here.


def index(request):
    return render(request, "index.html", {"questions" : QUESTIONS})


def question(request, i:int):
    return render(request, "question.html", {"questions" : QUESTIONS[i - 1]})
