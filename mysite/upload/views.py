from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views import View
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

class AlbumsView(View):
    albums = []
    albums_images = []
    albums_dict = dict()
    form = CreateNewAlbum
    initial = {'title': ''}
    template_name = 'upload/albums.html'

    def setup(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.albums = request.user.photoalbum_set.all()
        self.albums_images = []
        for album in self.albums:
            images = album.photo_set.first()
            self.albums_images.append(images)
        self.albums_dict = dict(zip(self.albums, self.albums_images))
        super()

    def get(self, request, *args, **kwargs):
        form = self.form(initial=self.initial)
        return render(request, self.template_name, {"form": form, "albums":self.albums, "albums_images":self.albums_images, "albums_dict":self.albums_dict})
    
    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            t = form.cleaned_data["title"]
            if(request.user.photoalbum_set.filter(title=t).exists()):
                messages.warning(request, "Album with the name <strong>'{0}'</strong> already exist! Please choose another name.".format(t), extra_tags="safe")
            else:
                newAlbum = request.user.photoalbum_set.create(title=t)
                messages.success(request, "New Album <strong>'{0}'</strong> Created! Click <a href='/album/{1}'>here</a> to view.".format(t, newAlbum.id), extra_tags="safe")
                self.albums = request.user.photoalbum_set.all()
        return render(request, self.template_name, {"form":form, "albums":self.albums, "albums_images":self.albums_images, "albums_dict":self.albums_dict})

@login_required
def album(response, id):
    photoalbum = response.user.photoalbum_set.get(id=id)
    return render(response, "upload/album.html", {"photoalbum":photoalbum})

def UserAlbumsList(response, username):
    the_user = User.objects.get(username = username)
    albums = the_user.photoalbum_set.all()
    return render(response, "upload/user_albums.html", {"albums":albums, "the_user":the_user})

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