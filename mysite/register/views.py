from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def register(response):
    if response.method == "POST":
        form = UserCreationForm(response.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()

    return render(response, "register/register.html", {"form":form})