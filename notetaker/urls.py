# authentication/urls.py
from django.conf.urls import url
from notetaker import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^notebooks$', views.notebooks, name='notebooks'),
    url(r'^documents$', views.documents, name='documents'),
    url(r'^tags$', views.tags, name='tags'),
    url(r'^(?P<note_id>[0-9]+)/$', views.noteedit, name='NoteEdit'),
]