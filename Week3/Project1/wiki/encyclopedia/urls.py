from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>/", views.wiki, name="wiki"),
    path("search/", views.search, name="search"),
    path("create/", views.create, name="create"),
    path("edit/<str:name>/", views.edit, name="edit"),
    path("rand/", views.rand, name="rand")
]
