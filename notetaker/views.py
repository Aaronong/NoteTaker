from django.shortcuts import render, HttpResponse

# Create your views here.


def index(request):
    return render(request, 'noteeditor.html')


def notebooks(request):
    return render(request, 'notebooks.html')


def documents(request):
    return render(request, 'documents.html')


def tags(request):
    return render(request, 'tags.html')


#search param can be document_id, tag_search, or word search
def noteedit(request,search_param):
    return render(request, 'noteeditor.html',search_param)

