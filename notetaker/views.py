from django.shortcuts import render, HttpResponse, render_to_response, redirect
from .models import *
from .forms import TextForm
from django.template import RequestContext

# Create your views here.


def index(request):
    form = TextForm()
    return render(request, 'index.html')


def notebooks(request):
    if request.method=='POST':
        title = request.POST.get('title')
        nb = Notebook(title=title, owner=NoteUser.objects.get_by_natural_key(request.user))
        nb.save()
        return redirect('/')
    all_notebooks = Notebook.objects.filter(owner=request.user)
    context = {
        'all_notebooks': all_notebooks,
    }
    # return HttpResponse({context})
    return render(request, 'notebooks.html', context)


def documents(request):
    if request.method=='POST':
        title = request.POST.get('title')
        nb_title = request.POST.get('selectnotebook')
        doc = Document(title=title, notebook=Notebook.objects.get(pk=nb_title))
        doc.save()
        thisuser = NoteUser.objects.get_by_natural_key(request.user)
        author = Authorization(user=thisuser, type=3, document=doc, initiator=thisuser)
        author.save()
        return redirect('/documents/')
    all_documents = Document.objects.filter(authorization__user=request.user)
    docs = {}
    for doc in all_documents:
        docs[doc] = NoteUser.objects.filter(authorization__document=doc, authorization__type=3)[0]
    all_notebooks = Notebook.objects.filter(owner=request.user)
    context = {
        'all_documents': docs,
        'all_notebooks': all_notebooks,
    }
    # return HttpResponse({context})
    return render(request, 'documents.html', context)


def notebook_edit(request, notebook_id):
    if request.method=='POST':
        title = request.POST.get('title')
        doc = Document(title=title, notebook=Notebook.objects.get(pk=notebook_id))
        doc.save()
        thisuser = NoteUser.objects.get_by_natural_key(request.user)
        author = Authorization(user=thisuser, type=3, document=doc, initiator=thisuser)
        author.save()
        return redirect('/notebooks/'+notebook_id+'/')
    documents_in_notebook = Document.objects.filter(notebook=notebook_id)
    docs = {}
    for doc in documents_in_notebook:
        docs[doc] = NoteUser.objects.filter(authorization__document=doc, authorization__type=3)[0]
    curr_notebook = Notebook.objects.get(pk=notebook_id)
    context = {
        'all_documents': docs,
        'notebook': curr_notebook,
    }
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
    if request.method=='POST':
        post_type = request.POST.get('post_type')
        note_ID = request.POST.get('noteid')
        note_TEXT = request.POST.get('notetext')

        # if edit do first block else second
        if post_type == 'edit':
            note_instance = Note.objects.get(pk=note_ID)
            note_instance.note_text = note_TEXT
            note_instance.save()

        else:
            doc_ID = request.POST.get('selectdoc')
            thisdoc = Document.objects.get(pk=doc_ID)
            new_note = Note(note_text=note_TEXT, document=thisdoc)
            new_note.save()
            thisuser = NoteUser.objects.get_by_natural_key(request.user)
            author = NoteAuthorization(user=thisuser, type=3, note=new_note, note_initiator=thisuser)
            author.save()

        return redirect('/noteedit/')
    all_notes = Note.objects.filter(noteauthorization__user=request.user)
    notes = {}
    all_documents = Document.objects.filter(authorization__user=request.user)
    for note in all_notes:
        author = NoteUser.objects.filter(noteauthorization__note=note, noteauthorization__type=3)[0]
        tags_in_note = Tags.objects.filter(tagging__note=note, tagging__note__noteauthorization__user=request.user)
        editing = False
        notes[note] = (author, tags_in_note, editing)
    context = {
        'all_notes': notes,
        'all_docs': all_documents,
    }
    return render(request, 'noteeditor.html', context)


def doc_edit(request, doc_id):

    if request.method=='POST':
        post_type = request.POST.get('post_type')
        note_ID = request.POST.get('noteid')
        note_TEXT = request.POST.get('notetext')

        # if edit do first block else second
        if post_type == 'edit':
            note_instance = Note.objects.get(pk=note_ID)
            note_instance.note_text = note_TEXT
            note_instance.save()
        else:
            doc_ID = doc_id
            thisdoc = Document.objects.get(pk=doc_ID)
            new_note = Note(note_text=note_TEXT, document=thisdoc)
            new_note.save()
            thisuser = NoteUser.objects.get_by_natural_key(request.user)
            author = NoteAuthorization(user=thisuser, type=3, note=new_note, note_initiator=thisuser)
            author.save()

        return redirect('/documents/'+doc_id+'/')

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


def tag_edit(request, tag_id):
    if request.method=='POST':
        post_type = request.POST.get('post_type')
        note_ID = request.POST.get('noteid')
        note_TEXT = request.POST.get('notetext')

        # if edit do first block else second
        if post_type == 'edit':
            note_instance = Note.objects.get(pk=note_ID)
            note_instance.note_text = note_TEXT
            note_instance.save()

        else:
            doc_ID = request.POST.get('selectdoc')
            thisdoc = Document.objects.get(pk=doc_ID)
            new_note = Note(note_text=note_TEXT, document=thisdoc)
            new_note.save()
            thisuser = NoteUser.objects.get_by_natural_key(request.user)
            author = NoteAuthorization(user=thisuser, type=3, note=new_note, note_initiator=thisuser)
            author.save()

        return redirect('/tags/'+tag_id+'/')
    tag_notes = Note.objects.filter(noteauthorization__user=request.user, tagging__tag=tag_id)
    notes = {}
    all_documents = Document.objects.filter(authorization__user=request.user)
    for note in tag_notes:
        author = NoteUser.objects.filter(noteauthorization__note=note, noteauthorization__type=3)[0]
        tags_in_note = Tags.objects.filter(tagging__note=note, tagging__note__noteauthorization__user=request.user)
        editing = False
        notes[note] = (author, tags_in_note,editing)
    context = {
        'all_notes': notes,
        'all_docs': all_documents,
    }
    return render(request, 'noteeditor.html', context)