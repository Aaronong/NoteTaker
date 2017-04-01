from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from django.core.serializers import serialize
from django.utils.safestring import mark_safe

from forms import ParentOrderForm, PauseResumeForm
from models import ParentOrder, ChildOrder
from threading import Thread

import json

@login_required(login_url="/")
def index(request):
    if request.method == 'POST':
        form = ParentOrderForm(request.POST)

        if form.is_valid():
            try:
                order = ParentOrder(
                    quantity = form.cleaned_data['quantity'], 
                    stock_type = "ACME ETF", 
                    is_sell = True,
                    user = request.user)
                if order.is_valid():
                    order.save()
                    api_response = order.query_market_datetime()
                    order.time_executed = api_response
                    order.save()  #second time is to save timestamp

                    t1 = Thread(target=order.trade)  # automatically try to execute trade upon submission
                    t1.daemon = True
                    t1.start()
                    return redirect('index')

                else:
                    form.add_error('quantity', 'Enter a whole number greater than zero.')

            except:
                form.add_error('quantity', '{:,d} is too large.'.format(form.cleaned_data['quantity']))

    else:
        form = ParentOrderForm()

    return render(request, 'place_order.html', {'form': form})

@login_required(login_url="/")
def order_detail(request, id):
    if request.method == 'POST':
        form = PauseResumeForm(request.POST)

        if form.is_valid():
            status_change = form.cleaned_data['status']

            if status_change == 'P':
                resume_order(request, id)
            elif status_change == 'S':
                pause_order(request, id)
            elif status_change == 'X':
                cancel_order(request, id)

    form = PauseResumeForm()

    parent = get_object_or_404(ParentOrder, id=id)

    try:
        children = ChildOrder.objects.filter(parent_order__id=id).order_by('-id')
    except ChildOrder.DoesNotExist:
        children = ChildOrder.objects.none()

    # total price, total sold, and average price
    parent_stats = parent.get_stats(children)

    return render(request, 'order_detail.html', 
        {
        'child_orders': children, 
        'parent_order': parent, 
        'total_price': '{:,.2f}'.format(parent_stats['total_price']), 
        'total_sold': '{:,d}'.format(parent_stats['total_quantity']), 
        'average_price': '{:,.2f}'.format(parent_stats['average_price']), 
        'form': form
        })

def get_progress(request, id):
    parent = get_object_or_404(ParentOrder, id=id)
    current_progress = '{:,.2f}'.format(parent.progress)
    return HttpResponse(current_progress)

def get_status(request, id):
    parent = get_object_or_404(ParentOrder, id=id)
    return HttpResponse(parent.status)

def get_children(request, id, child_id):
    parent = get_object_or_404(ParentOrder, id=id)
    try:
        children = ChildOrder.objects.filter(parent_order__id=id)
    except ChildOrder.DoesNotExist:
        children = ChildOrder.objects.none()
    parent_stats = parent.get_stats(children)
    parent_stats["average_price"] = '{:,.2f}'.format(parent_stats["average_price"])
    parent_stats["total_price"] = '{:,.2f}'.format(parent_stats["total_price"])
    return_dict = {"children": json.loads(serialize('json', children.filter(id__gt=child_id))), "stats": parent_stats}
    return HttpResponse(mark_safe(json.dumps(return_dict, ensure_ascii=False)))

def get_children_undefined(request, id):
    parent = get_object_or_404(ParentOrder, id=id)
    try:
        children = ChildOrder.objects.filter(parent_order__id=id)
    except ChildOrder.DoesNotExist:
        children = ChildOrder.objects.none()
    parent_stats = parent.get_stats(children)
    parent_stats["average_price"] = '{:,.2f}'.format(parent_stats["average_price"])
    parent_stats["total_price"] = '{:,.2f}'.format(parent_stats["total_price"])
    return_dict = {"children": json.loads(serialize('json', children)), "stats": parent_stats}
    return HttpResponse(mark_safe(json.dumps(return_dict, ensure_ascii=False)))

def pause_order(request, id):
    parent = get_object_or_404(ParentOrder, id=id)
    parent.status = ParentOrder.PAUSED
    parent.save()

def cancel_order(request, id):
    parent = get_object_or_404(ParentOrder, id=id)
    parent.status = ParentOrder.CANCELLED
    parent.save()

def resume_order(request, id):
    parent = get_object_or_404(ParentOrder, id=id)
    if(parent.status != ParentOrder.PAUSED):  # We can only resume orders that are paused
        return False
    parent.status = ParentOrder.IN_PROGRESS
    parent.update_progress()
    parent.save()
    t1 = Thread(target=parent.trade)  # automatically try to execute trade upon submission
    t1.daemon = True
    t1.start()
    return redirect('index')
