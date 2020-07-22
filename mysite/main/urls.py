from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("list/", views.allList, name="allList"),
    path("list/<int:id>", views.list, name="list"),
    path("create/", views.create, name="create"),
    path("albums/", views.albums, name="albums"),
    path("album/<int:id>", views.album, name="album"),
    path("upload/", views.upload, name="upload"),
]
#path("<int:id>", views.index, name="index"),