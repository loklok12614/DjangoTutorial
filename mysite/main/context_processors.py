from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
import urllib
from main.views import get_queryset


def add_variable_to_context(request):
    context = {}
    context['profiles'] = User.objects.all()
    # query = ""
    # if request.GET:
    #     if(request.GET['q']):
    #         query = request.GET['q']
    #         context['query'] = str(query)
    #         profiles = get_queryset(query)
    #         context['profiles'] = profiles
        # return HttpResponseRedirect(reverse("main:list", kwargs=context))
            # return HttpResponseRedirect("/list/")
    return context