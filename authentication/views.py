from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from stocks.models import ParentOrder, ChildOrder

@login_required(login_url="login/")
def index(request):
    order_list = ParentOrder.objects.all().order_by('-id')
    for order in order_list:
        children = ChildOrder.objects.filter(parent_order__id=order.id)
        # get stats
        order_stats = order.get_stats(children)
        # format stats
        order.avg_price = '{:,.2f}'.format(order_stats['average_price'])
        order.progress = '{:,.2f}'.format(order.progress)

    context_dict = {'orders': order_list}

    # render homepage
    return render(request, "index.html", context_dict)