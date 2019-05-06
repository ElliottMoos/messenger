from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('home', views.home),
    path('message/<int:person_id>', views.create),
    path('home/change/<int:new_id>', views.change),
    path('home/clear_receiver', views.clear),
    path('search', views.search),
    path('logout', views.logout),
]