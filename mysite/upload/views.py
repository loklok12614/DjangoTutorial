from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import PhotoAlbum, Photo
from .forms import CreateNewAlbum, UploadFileForm

# Create your views here.
@login_required
def albums(response):
    albums = response.user.photoalbum_set.all()
    # albums = PhotoAlbum.objects.all()
    if response.method == "POST":
        form = CreateNewAlbum(response.POST)
        if form.is_valid():
            t = form.cleaned_data["title"]
            newAlbum = response.user.photoalbum_set.create(title=t)
            messages.success(response, "New Album <strong>'{0}'</strong> Created! Click <a href='/album/{1}'>here</a> to view.".format(t, newAlbum.id), extra_tags="safe")
    else:
        form = CreateNewAlbum()
    
    return render(response, "upload/albums.html", {"albums":albums, "form":form})

@login_required
def album(response, id):
    photoalbum = response.user.photoalbum_set.get(id=id)
    return render(response, "upload/album.html", {"photoalbum":photoalbum})

@login_required
def upload(response):
    albumid = id
    if (response.method == "POST"):
        form = UploadFileForm(response.user, response.POST, response.FILES)
        if form.is_valid():
            album = form.cleaned_data["album"]
            photoalbum = response.user.photoalbum_set.get(title=album)
            caption = form.cleaned_data["caption"]
            img = response.FILES['img']
            photo = photoalbum.photo_set.create(caption=caption, img=img)
            messages.success(response, "Image uploaded.", extra_tags="safe")
    else:
        form = UploadFileForm(response.user)
    return render(response, "upload/upload.html", {"form":form, "albumid": albumid})

def UserAlbumsList(response, pk):
    user = User.objects.get(pk= pk)
    albums = user.photoalbum_set.all()
    return render(response, "upload/user_albums.html", {"albums":albums})