from django.shortcuts import render, HttpResponse, render_to_response
from .models import *
from .forms import TextForm
from django.template import RequestContext

# Create your views here.


def index(request):
    form = TextForm()
    return render(request, 'index.html')


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
    all_tags = Tags.objects.filter(tagging__note__noteauthorization__user=request.user)
    tag_with_notes = {}
    for tag in all_tags:
        tag_with_notes[tag] = Note.objects.filter(noteauthorization__user=request.user, tagging__tag=tag)
    context = {
        'all_tags': tag_with_notes,
    }
    # return HttpResponse({context})
    return render(request, 'tags.html', context)


# search param can be document_id, tag_search, or word search
def noteedit(request):
    all_notes = Note.objects.filter(noteauthorization__user=request.user)
    notes = {}
    for note in all_notes:
        author = NoteUser.objects.filter(noteauthorization__note=note, noteauthorization__type=3)[0]
        tags_in_note = Tags.objects.filter(tagging__note=note, tagging__note__noteauthorization__user=request.user)
        editing = False
        notes[note] = (author, tags_in_note, editing)
    context = {
        'all_notes': notes,
    }
    return render(request, 'noteeditor.html', context)


def doc_edit(request, doc_id):
    doc_notes = Note.objects.filter(noteauthorization__user=request.user, document=doc_id)
    notes = {}
    for note in doc_notes:
        author = NoteUser.objects.filter(noteauthorization__note=note, noteauthorization__type=3)[0]
        tags_in_note = Tags.objects.filter(tagging__note=note, tagging__note__noteauthorization__user=request.user)
        editing = False
        notes[note] = (author, tags_in_note, editing)
    context = {
        'all_notes': notes,
    }
    return render(request, 'noteeditor.html', context)


def notebook_edit(request, notebook_id):
    documents_in_notebook = Document.objects.filter(notebook=notebook_id)
    docs = {}
    for doc in documents_in_notebook:
        docs[doc] = NoteUser.objects.filter(authorization__document=doc, authorization__type=3)[0]
    context = {
        'all_documents': docs,
    }
    return render(request, 'documents.html', context)


def tag_edit(request, tag_id):
    tag_notes = Note.objects.filter(noteauthorization__user=request.user, tagging__tag=tag_id)
    notes = {}
    for note in tag_notes:
        author = NoteUser.objects.filter(noteauthorization__note=note, noteauthorization__type=3)[0]
        tags_in_note = Tags.objects.filter(tagging__note=note, tagging__note__noteauthorization__user=request.user)
        editing = False
        notes[note] = (author, tags_in_note,editing)
    context = {
        'all_notes': notes,
    }
    return render(request, 'noteeditor.html', context)