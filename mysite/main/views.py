from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import ToDoList, Item, Item1, MovieList, Movie
from .form import CreateNewList

# Create your views here.
def index(response):
    return render(response, "main/base.html", {})

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
    context = {}
    context['ls'] = response.user.todolist_set.all()
    return render(response, "main/allList.html", context)

@login_required
def list(response, id):
    # ls = ToDoList.objects.get(id=id)
    context = {}
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
    context['ls'] = ls
    return render(response, "main/list.html", context)
    
def home(response):
    context = {}
    return render(response, "main/home.html", context)

@login_required
def create(response):
    context = {}
    if response.method == "POST":
        form = CreateNewList(response.POST)
        if form.is_valid():
            n = form.cleaned_data["name"]
            l = response.user.todolist_set.create(name=n)
            messages.success(response, "New List <strong>'{0}'</strong> Created! Click <a href='/list/{1}'>here</a> to view.".format(n, l.id), extra_tags="safe")
        return HttpResponseRedirect("/list/%i" %l.id)
    else:
        form = CreateNewList()
    context['form'] = form
    return render(response, "main/create.html", context)