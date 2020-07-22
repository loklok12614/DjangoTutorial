from django import forms
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import PhotoAlbum, Photo

class CreateNewList(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    check = forms.BooleanField(required=False)

class CreateNewAlbum(forms.Form):
    title = forms.CharField(label="Title", max_length=200)

class UploadFileForm(forms.ModelForm):
    album = forms.ModelChoiceField(queryset=PhotoAlbum.objects.all().order_by('title'))
    caption = forms.CharField(max_length=255)
    img = forms.ImageField(label="Select a file", help_text="max. 42megabytes")
    class Meta:
        model = Photo
        fields = ('album', 'caption', 'img')

    def __init__(self, user, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.fields['album'].queryset = PhotoAlbum.objects.filter(user=user)