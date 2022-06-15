"""WEB_Questions_Service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import views
from django.conf import settings
from django.contrib import admin
from django.urls import path
from app import views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.index, name="home"),
    path('<int:page>', views.new_question, name="new"),
    path('hot/<int:page>', views.hot, name="hot"),
    path('tag/<int:j>/<int:page>', views.tag, name="tag_url"),
    path('question/<int:i>/<int:page>', views.question, name="question_url"),
    path('ask/',views.ask, name="ask"),
    path('profile/<int:i>', views.profile, name="profile_url"),
    path('log_out', views.log_out, name="log_out"),
    path('login', views.log_in, name="login"),
    path('register', views.register, name="register"),
    path('question_vote/', views.question_vote, name="question_vote"),
    path('answer_vote/', views.answer_vote, name='answer_vote'),
    path('checkbox_vote/', views.checkbox_vote, name='checkbox_vote'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)