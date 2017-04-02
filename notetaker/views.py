from django.shortcuts import render
from .models import *

# Create your views here.


def index(request):
    return render(request, 'tags.html')


def notebooks(request):
    all_notebooks = Notebook.objects.filter(owner=request.user)
    context = {
        'all_notebooks': all_notebooks,
    }
    # return HttpResponse({context})
    return render(request, 'notebooks.html', context)


def documents(request):
    all_documents = Document.objects.filter(authorization__user=request.user)
    docs = {}
    for doc in all_documents:
        docs[doc] = NoteUser.objects.filter(authorization__document=doc, authorization__type=3)[0]
    context = {
        'all_documents': docs,
    }
    # return HttpResponse({context})
    return render(request, 'documents.html', context)


def tags(request):
    all_documents = Document.objects.filter(authorization__user=request.user)
    all_notes = Note.objects.f
    return render(request, 'tags.html')


#search param can be document_id, tag_search, or word search
def noteedit(request,search_param):
    return render(request, 'noteeditor.html',search_param)

