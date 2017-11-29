from django.conf.urls import *
from . import views

from newsapp.views import IndexView

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^news_detail/(?P<pk>\d+)/$', views.NewsDetailView.as_view(), name='news_detail'),
    # url(r'^news_detail/(?P<pk>\d+)/$', views.news_detail, name='news_detail'),
    url(r'^search/$', views.SearchView.as_view(), name='search'),
    # url(r'^search/$', views.search, name='search'),
    # url(r'^news/new/$', views.news_new, name='news_new'),
    url(r'^news/new/$', views.NewNewsView.as_view(), name='news_new'),

    url(r'^users/', include('django.contrib.auth.urls')),
    url(r'^news/(?P<pk>\d+)/comment/$', views.add_comment, name='add_comment'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
]
