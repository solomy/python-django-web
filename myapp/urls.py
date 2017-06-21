"""moneyweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from app.views import login,details_yewu,browse_ever_yewu,register, insert_yewu,update_people,update_search,\
    main,login_error,logout,inset_people,browse_people,browse_salary,daka,qiandao,qiantui,browse_ever_people,browse_ever_salary,search_people,permiss_yewu,pay,print_pay,chang_ps
#from moneyweb import settings
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^details_yewu/$', details_yewu),
    url(r'^main/$', main),
     url(r'^login/$', login),
    url(r'^register/$', register),
    url(r'^login_error/$', login_error),
    url(r'^logout/$', logout),
    url(r'^chang_ps/$',chang_ps),

    url(r'^insert_people/$', inset_people),
    url(r'^insert_yewu/$', insert_yewu),
    url(r'^show_people/$', browse_people),
    url(r'^show_ever_people/$', browse_ever_people),
    url(r'^show_salary/$', browse_salary),
    url(r'^show_ever_salary/$', browse_ever_salary),
    url(r'^show_ever_yewu/$', browse_ever_yewu),

    url(r'^search_people/$', search_people),

    url(r'^update_search/$', update_search),
    url(r'^update_people/$', update_people),

    url(r'^permiss_yewu/$', permiss_yewu),
    url(r'^pay/$', pay),
    url(r'^print_pay/$', print_pay),

    url(r'^daka/$', daka),
    url(r'^qiandao/$',qiandao),
    url(r'^qiantui/$',qiantui),
  #  url(r'^static/(?P<path>.*)$', 'django.view.static.serve', {'docment_root':settings.STATICFILES_DIRS,'show_indexes':True}),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
