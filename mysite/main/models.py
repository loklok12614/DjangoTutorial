from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ToDoList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
class Item(models.Model):
    todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    complete = models.BooleanField()

    def __str__(self):
        return self.text

class Item1(models.Model):
    todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    complete = models.BooleanField()

    def __str__(self):
        return self.text

class MovieList(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Movie(models.Model):
    movielist = models.ForeignKey(MovieList, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    poster = models.ImageField(upload_to='movies', default="/icon8-box-64.jpg")
    def __str__(self):
        return self.title

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