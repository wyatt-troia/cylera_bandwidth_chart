from django.urls import path

from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('get_chart_data', views.get_chart_data, name='get_chart_data')
]
