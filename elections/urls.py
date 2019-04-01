from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.urls import include
from . import views

app_name = 'elections'
urlpatterns = [
    path('', views.index, name='home'),
    path('areas/<str:area>/', views.areas),
    path('areas/<str:area>/results', views.results),
    path('polls/<int:poll_id>', views.polls),
    path('candidates/<str:name>/', views.candidates),
]
