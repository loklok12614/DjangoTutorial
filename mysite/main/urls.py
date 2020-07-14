from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home/", views.home, name="home"),
    path("list/", views.allList, name="allList"),
    path("list/<int:id>", views.list, name="list"),
    path("create/", views.create, name="create"),
]
#path("<int:id>", views.index, name="index"),