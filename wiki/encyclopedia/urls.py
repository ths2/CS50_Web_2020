from django.urls import path

from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
   
    path("wiki", views.index, name="index"),
    path("wiki/create/newpage", views.new_page, name="new"),
    path("wiki/<str:name>", views.page, name="page"),
    path("", RedirectView.as_view(pattern_name='index', permanent=False)), 
]
