from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from stocks.models import ParentOrder, ChildOrder


def index(request):
    return render(request, 'tags.html')