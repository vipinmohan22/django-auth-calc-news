from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^calc_op/$', views.calc_op, name='calc_op'),
]
