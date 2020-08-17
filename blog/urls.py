from django.contrib import admin
from django.urls import path
from blog import views
# import forms_builder.forms.urls

app_name='blog'

urlpatterns = [
    path('', views.allblogs, name='allblogs'),
    path('<int:blog_id>/', views.detail, name='detail'),
]
