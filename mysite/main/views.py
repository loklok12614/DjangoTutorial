from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item, Item1
from .form import CreateNewList

# Create your views here.

def index(response, id):
    ls = ToDoList.objects.get(id=id)
    my_dict = {"name": ls.name}
    item_counter = 1
    for x in ls.item_set.all():
        item_name = "item" + str(item_counter)
        my_dict[item_name] = x
        item_counter = item_counter + 1
    return render(response, "main/base.html", my_dict)

def index1(response, name):
    ls = ToDoList.objects.get(name=name)
    #item = ls.item_set.create(text="Buy apples", complete=False)
    items = ls.item_set.all()
    return HttpResponse("<h1>%s</h1>"
                        "</br>"
                        "<p>%s</p>" %(ls.name,items[0].text))

def allList(response):
    ls = ToDoList.objects
    return render(response, "main/allList.html", {"ls":ls})

def list(response, id):
    ls = ToDoList.objects.get(id=id)
    return render(response, "main/list.html", {"ls":ls})

def home(response):
    return render(response, "main/home.html", {})

def create(response):
    if response.method == "POST":
        form = CreateNewList(response.POST)
        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name=n)
            t.save()
            messages.info(response, "New List - %s - Created!" %n)
        #return render(response, "main/create.html", {"form":form, "message":message})
        #return HttpResponseRedirect("/list/%i" %t.id)
    else:
        form = CreateNewList()
    return render(response, "main/create.html", {"form":form})