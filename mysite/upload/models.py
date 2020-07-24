from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PhotoAlbum(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Photo(models.Model):
    photoalbum = models.ForeignKey(PhotoAlbum, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='photos', null=True)
    caption = models.CharField(max_length=255)
    def __str__(self):
        return self.caption