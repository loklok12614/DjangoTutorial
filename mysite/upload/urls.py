from django.urls import path

from . import views
from .views import AlbumsView

urlpatterns = [
    path("albums/", AlbumsView.as_view(), name="albums"),
    # path("albums/", views.albums, name="albums"),
    path("albums/users/<int:pk>", views.UserAlbumsList, name="user_albums"),
    path("album/<int:id>", views.album, name="album"),
    path("upload/", views.upload, name="upload"),
]