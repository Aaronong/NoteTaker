# authentication/urls.py
from django.conf.urls import url
from notetaker import views
from django.contrib import admin
from django.contrib.auth import views as auth_views
from authentication.forms import LoginForm

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/login'}, name='logout'),
    url(r'^notebooks/$', views.notebooks, name='notebooks'),
    url(r'^documents/$', views.documents, name='documents'),
    url(r'^tags/$', views.tags, name='tags'),
url(r'^noteedit/$', views.noteedit, name='NoteEdit'),
    url(r'^(?P<note_id>[0-9]+)/$', views.noteedit, name='NoteEdit'),
]