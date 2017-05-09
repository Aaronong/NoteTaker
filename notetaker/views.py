from django.shortcuts import render, HttpResponse, redirect
from .models import *
from social_django.models import UserSocialAuth, DjangoStorage, USER_MODEL


# Create your views here.


def index(request):
    try:
        owner = NoteUser.objects.get_by_natural_key(request.user)
    except:
        new_User = NoteUser(request.user)
        new_User.save()
    return redirect('/notebooks')


def testbed(request):
    return render(request, 'index.html')


def friends(request):
    social_user = UserSocialAuth.objects.filter(user_id=request.user.id)
    if len(social_user) == 0:
        social_user = "Not a social user"
    else:
        social_user = social_user[0]

    context = {
        'social_user': social_user,
    }
    return render(request, 'friends.html', context)


def notebooks(request):
    if request.method=='POST':
        post_type = request.POST.get('post_type')
        if post_type == 'new':
            title = request.POST.get('title')
            nb = Notebook(title=title, owner=NoteUser.objects.get_by_natural_key(request.user))
            nb.save()

        elif post_type == 'del':
            notebook_ID = request.POST.get('notebookid')
            Notebook.objects.get(pk=notebook_ID).delete()
        return redirect('/notebooks')
    all_notebooks = Notebook.objects.filter(owner=request.user)
    context = {
        'all_notebooks': all_notebooks,
    }
    # return HttpResponse({context})
    return render(request, 'notebooks.html', context)


def documents(request):
    if request.method=='POST':
        post_type = request.POST.get('post_type')

        if post_type == 'create':
            title = request.POST.get('title')
            nb_title = request.POST.get('selectnotebook')
            doc = Document(title=title, notebook=Notebook.objects.get(pk=nb_title))
            doc.save()
            thisuser = NoteUser.objects.get_by_natural_key(request.user)
            author = Authorization(user=thisuser, type=3, document=doc, initiator=thisuser)
            author.save()

        elif post_type == 'ppl':
            doc_ID = request.POST.get('docid')
            person = request.POST.get('person')
            authtype = request.POST.get('authtype')
            change_authorization(NoteUser.objects.get(pk=person), Document.objects.get(pk=doc_ID), int(authtype))

        elif post_type == 'del':
            doc_ID = request.POST.get('docid')
            Document.objects.get(pk=doc_ID).delete()

        return redirect('/documents/')

    all_documents = Document.objects.filter(authorization__user=request.user)
    docs = {}
    for doc in all_documents:
        docs[doc] = NoteUser.objects.filter(authorization__document=doc, authorization__type=3)[0]
    all_notebooks = Notebook.objects.filter(owner=request.user)
    all_users = NoteUser.objects.all()
    context = {
        'all_documents': docs,
        'all_notebooks': all_notebooks,
        'all_users': all_users,
    }
    # return HttpResponse({context})
    return render(request, 'documents.html', context)


def notebook_edit(request, notebook_id):
    if request.method=='POST':
        post_type = request.POST.get('post_type')

        if post_type == 'create':
            title = request.POST.get('title')
            doc = Document(title=title, notebook=Notebook.objects.get(pk=notebook_id))
            doc.save()
            thisuser = NoteUser.objects.get_by_natural_key(request.user)
            author = Authorization(user=thisuser, type=3, document=doc, initiator=thisuser)
            author.save()

        elif post_type == 'ppl':
            doc_ID = request.POST.get('docid')
            person = request.POST.get('person')
            authtype = request.POST.get('authtype')
            change_authorization(NoteUser.objects.get(pk=person), Document.objects.get(pk=doc_ID), int(authtype))

        elif post_type == 'del':
            doc_ID = request.POST.get('docid')
            Document.objects.get(pk=doc_ID).delete()

        return redirect('/notebooks/'+notebook_id+'/')

    documents_in_notebook = Document.objects.filter(notebook=notebook_id)
    docs = {}
    for doc in documents_in_notebook:
        docs[doc] = NoteUser.objects.filter(authorization__document=doc, authorization__type=3)[0]
    curr_notebook = Notebook.objects.get(pk=notebook_id)
    all_users = NoteUser.objects.all()
    context = {
        'all_documents': docs,
        'notebook': curr_notebook,
        'all_users': all_users,
    }
    return render(request, 'documents.html', context)


def tags(request):
    all_tags = Tags.objects.filter(tagging__note__noteauthorization__user=request.user).order_by('tag_text')
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
            edit_notetext(note_instance, note_TEXT)

        elif post_type == 'ppl':
            person = request.POST.get('person')
            authtype = request.POST.get('authtype')
            change_note_authorization(NoteUser.objects.get(pk=person), Note.objects.get(pk=note_ID), int(authtype))

        elif post_type == 'tag':
            tag_text = request.POST.get('tagtext')
            thisuser = NoteUser.objects.get_by_natural_key(request.user)
            if get_tag(tag_text):
                create_tagging(Note.objects.get(pk=note_ID), get_tag(tag_text), thisuser)
            else:
                make_tag(tag_text, Note.objects.get(pk=note_ID), thisuser)

        elif post_type == 'del':
            note_ID = request.POST.get('noteid')
            Note.objects.get(pk=note_ID).delete()

        else:
            doc_ID = request.POST.get('selectdoc')
            thisuser = NoteUser.objects.get_by_natural_key(request.user)
            create_new_note(doc_ID, note_TEXT, thisuser)

        return redirect('/noteedit/')
    all_notes = Note.objects.filter(noteauthorization__user=request.user)
    notes = {}
    all_documents = Document.objects.filter(authorization__user=request.user)
    for note in all_notes:
        author = NoteUser.objects.filter(noteauthorization__note=note, noteauthorization__type=3)[0]
        tags_in_note = Tags.objects.filter(tagging__note=note, tagging__note__noteauthorization__user=request.user)
        editing = False
        notes[note] = (author, tags_in_note, editing)
    all_users = NoteUser.objects.all()
    context = {
        'all_notes': notes,
        'all_docs': all_documents,
        'all_users': all_users,
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
            edit_notetext(note_instance, note_TEXT)

        elif post_type == 'ppl':
            person = request.POST.get('person')
            authtype = request.POST.get('authtype')
            change_note_authorization(NoteUser.objects.get(pk=person), Note.objects.get(pk=note_ID), int(authtype))

        elif post_type == 'tag':
            tag_text = request.POST.get('tagtext')
            thisuser = NoteUser.objects.get_by_natural_key(request.user)
            if get_tag(tag_text):
                create_tagging(Note.objects.get(pk=note_ID), get_tag(tag_text), thisuser)
            else:
                make_tag(tag_text, Note.objects.get(pk=note_ID), thisuser)

        elif post_type == 'del':
            note_ID = request.POST.get('noteid')
            Note.objects.get(pk=note_ID).delete()

        else:
            doc_ID = doc_id
            thisuser = NoteUser.objects.get_by_natural_key(request.user)
            create_new_note(doc_ID, note_TEXT, thisuser)

        return redirect('/documents/'+doc_id+'/')

    doc_notes = Note.objects.filter(noteauthorization__user=request.user, document=doc_id)
    notes = {}
    for note in doc_notes:
        author = NoteUser.objects.filter(noteauthorization__note=note, noteauthorization__type=3)[0]
        tags_in_note = Tags.objects.filter(tagging__note=note, tagging__note__noteauthorization__user=request.user)
        editing = False
        notes[note] = (author, tags_in_note, editing)
    all_users = NoteUser.objects.all()
    context = {
        'all_notes': notes,
        'all_users': all_users,
    }
    return render(request, 'noteeditor.html', context)


def tag_edit(request, tag_id):
    if request.method=='POST':
        post_type = request.POST.get('post_type')
        note_ID = request.POST.get('noteid')
        note_TEXT = request.POST.get('notetext')

        if post_type == 'tag':
            tag_text = request.POST.get('tagtext')
            thisuser = NoteUser.objects.get_by_natural_key(request.user)
            if get_tag(tag_text):
                create_tagging(Note.objects.get(pk=note_ID), get_tag(tag_text), thisuser)
            else:
                make_tag(tag_text, Note.objects.get(pk=note_ID), thisuser)

        # if edit do first block else second
        elif post_type == 'edit':
            note_instance = Note.objects.get(pk=note_ID)
            edit_notetext(note_instance, note_TEXT)

        elif post_type == 'ppl':
            person = request.POST.get('person')
            authtype = request.POST.get('authtype')
            change_note_authorization(NoteUser.objects.get(pk=person), Note.objects.get(pk=note_ID), int(authtype))

        elif post_type == 'del':
            note_ID = request.POST.get('noteid')
            Note.objects.get(pk=note_ID).delete()

        else:
            doc_ID = request.POST.get('selectdoc')
            thisuser = NoteUser.objects.get_by_natural_key(request.user)
            create_new_note(doc_ID, note_TEXT, thisuser)


        return redirect('/tags/'+tag_id+'/')
    tag_notes = Note.objects.filter(noteauthorization__user=request.user, tagging__tag=tag_id)
    notes = {}
    all_documents = Document.objects.filter(authorization__user=request.user)
    for note in tag_notes:
        author = NoteUser.objects.filter(noteauthorization__note=note, noteauthorization__type=3)[0]
        tags_in_note = Tags.objects.filter(tagging__note=note, tagging__note__noteauthorization__user=request.user)
        editing = False
        notes[note] = (author, tags_in_note,editing)
    all_users = NoteUser.objects.all()
    context = {
        'all_notes': notes,
        'all_docs': all_documents,
        'all_users': all_users,
    }
    return render(request, 'noteeditor.html', context)