from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import ToDoList, Item, Item1, MovieList, Movie, PhotoAlbum, Photo
from .form import CreateNewList, CreateNewAlbum, UploadFileForm

from PIL import Image


# Create your views here.

@login_required
def index(response, id):
    ls = ToDoList.objects.get(id=id)
    my_dict = {"name": ls.name}
    item_counter = 1
    for x in ls.item_set.all():
        item_name = "item" + str(item_counter)
        my_dict[item_name] = x
        item_counter = item_counter + 1
    return render(response, "main/base.html", my_dict)

@login_required
def index1(response, name):
    ls = ToDoList.objects.get(name=name)
    #item = ls.item_set.create(text="Buy apples", complete=False)
    items = ls.item_set.all()
    return HttpResponse("<h1>%s</h1>"
                        "</br>"
                        "<p>%s</p>" %(ls.name, items[0].text))

@login_required
def allList(response):
    ls = response.user.todolist_set.all()
    return render(response, "main/allList.html", {"ls":ls})

@login_required
def list(response, id):
    # ls = ToDoList.objects.get(id=id)
    ls = get_object_or_404(ToDoList, id=id)
    if response.method == "POST":
        if response.POST.get("save"):
            for item in ls.item_set.all():
                if response.POST.get("c" + str(item.id)):
                    item.complete = True
                else:
                    item.complete = False
                item.text = response.POST.get("t" + str(item.id))
                item.save()
            
        elif response.POST.get("newItem"):
            txt = response.POST.get("new")

            if len(txt) > 2:
                ls.item_set.create(text=txt, complete=False)
                messages.success(response, "Item <strong>%s</strong> has been added!" %txt, extra_tags="safe")
            else:
                print("Invalid")

        elif response.POST.get("saveNameBtn"):
            newName = response.POST.get("newName")
            ls.name = newName
            ls.save()
            messages.success(response, "List's name has been changed!", extra_tags="safe")

        #handle delete item
        for item in ls.item_set.all():
            if response.POST.get("delete" + str(item.id)):
                item.delete()
                messages.info(response, "Item <strong>%s</strong> has been deleted!" %item.text, extra_tags="safe")
    return render(response, "main/list.html", {"ls":ls})

@login_required
def home(response):
    return render(response, "main/home.html", {})

@login_required
def create(response):
    if response.method == "POST":
        form = CreateNewList(response.POST)
        if form.is_valid():
            n = form.cleaned_data["name"]
            l = response.user.todolist_set.create(name=n)
            messages.success(response, "New List <strong>'{0}'</strong> Created! Click <a href='/list/{1}'>here</a> to view.".format(n, l.id), extra_tags="safe")
        #return HttpResponseRedirect("/list/%i" %t.id)
    else:
        form = CreateNewList()
    return render(response, "main/create.html", {"form":form})

@login_required
def albums(response):
    albums = response.user.photoalbum_set.all()
    if response.method == "POST":
        form = CreateNewAlbum(response.POST)
        if form.is_valid():
            t = form.cleaned_data["title"]
            newAlbum = response.user.photoalbum_set.create(title=t)
            messages.success(response, "New Album <strong>'{0}'</strong> Created! Click <a href='/album/{1}'>here</a> to view.".format(t, newAlbum.id), extra_tags="safe")
    else:
        form = CreateNewAlbum()
    
    return render(response, "main/albums.html", {"albums":albums, "form":form})

@login_required
def album(response, id):
    photoalbum = response.user.photoalbum_set.get(id=id)
    return render(response, "main/album.html", {"photoalbum":photoalbum})

@login_required
def upload(response):
    albumid = id
    if (response.method == "POST"):
        form = UploadFileForm(response.user, response.POST, response.FILES)
        # form.photoalbum.queryset = response.user.photoalbum_set.all().order_by('title')
        if form.is_valid():
            album = form.cleaned_data["album"]
            photoalbum = response.user.photoalbum_set.get(title=album)
            caption = form.cleaned_data["caption"]
            img = response.FILES['img']
            photo = photoalbum.photo_set.create(caption=caption, img=img)
            messages.success(response, "Image uploaded.", extra_tags="safe")
    else:
        form = UploadFileForm(response.user)
    return render(response, "main/upload.html", {"form":form, "albumid": albumid})