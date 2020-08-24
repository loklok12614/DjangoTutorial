from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
import urllib

import json
from django.core.serializers.json import DjangoJSONEncoder

from main.views import get_queryset


def add_variable_to_context(request):
    context = {}
    profiles = User.objects.all().values_list('username', 'email')
    profiles_json = json.dumps(list(profiles), cls=DjangoJSONEncoder)
    context["profiles"] = profiles_json

    # context['profiles'] = [{'username': profile.username, 'email': profile.email} for profile in profiles]
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