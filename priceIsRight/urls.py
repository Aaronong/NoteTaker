"""priceIsRight URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from authentication.forms import LoginForm
from stocks import views

urlpatterns = [
    url(r'auth', include('authentication.urls')),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/login'}, name='logout'),
    url(r'', include('notetaker.urls')),
    url(r'^place_order/$', views.index, name='place_order'),
    url(r'^order/(?P<id>[0-9]+)/$', views.order_detail, name='order_detail'),
    url(r'^admin/', admin.site.urls),
    url(r'^order/(?P<id>[0-9]+)/get_progress/$', views.get_progress, name='get_progress'),
    url(r'^order/(?P<id>[0-9]+)/get_status/$', views.get_status, name='get_status'),
    url(r'^order/(?P<id>[0-9]+)/get_children/(?P<child_id>[0-9]+)/$', views.get_children, name='get_children'),
    url(r'^order/(?P<id>[0-9]+)/get_children/undefined/$', views.get_children_undefined, name='get_children_undefined'),
]


#
# urlpatterns = [
#     url(r'notetaker', include('notetaker.urls')),
#     url(r'auth', include('authentication.urls')),
#     url(r'^login/$', auth_views.login, {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
#     url(r'^logout/$', auth_views.logout, {'next_page': '/login'}, name='logout'),
#     url(r'^place_order/$', views.index, name='place_order'),
#     url(r'^order/(?P<id>[0-9]+)/$', views.order_detail, name='order_detail'),
#     url(r'^admin/', admin.site.urls),
#     url(r'^order/(?P<id>[0-9]+)/get_progress/$', views.get_progress, name='get_progress'),
#     url(r'^order/(?P<id>[0-9]+)/get_status/$', views.get_status, name='get_status'),
#     url(r'^order/(?P<id>[0-9]+)/get_children/(?P<child_id>[0-9]+)/$', views.get_children, name='get_children'),
#     url(r'^order/(?P<id>[0-9]+)/get_children/undefined/$', views.get_children_undefined, name='get_children_undefined'),
# ]
