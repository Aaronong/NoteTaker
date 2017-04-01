# authentication/urls.py
from django.conf.urls import url
from notetaker import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]