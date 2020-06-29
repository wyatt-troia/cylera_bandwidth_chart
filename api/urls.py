from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('get_bandwidths', views.get_bandwidths, name='get_bandwidths')
]
