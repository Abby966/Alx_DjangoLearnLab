from django.urls import path
from . import views
from .views import example_form_view

urlpatterns = [
    path('', views.index, name='index'),  # This will serve /books/
    path('example-form/', example_form_view, name='example-form'),
]
