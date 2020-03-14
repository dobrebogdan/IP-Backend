from django.urls import path

from . import views

urlpatterns = [
    path('poll/<id>', views.poll, name='poll'),
    path('get/<id>', views.get, name='get'),
    path('put', views.put, name='put'),
]