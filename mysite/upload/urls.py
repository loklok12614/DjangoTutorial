from django.urls import path

from . import views

urlpatterns = [
    path("albums/", views.albums, name="albums"),
    path("album/<int:id>", views.album, name="album"),
    path("upload/", views.upload, name="upload"),
]