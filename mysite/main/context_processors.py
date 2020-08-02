from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect


def add_variable_to_context(request):
    context = {}

    query = ""
    if request.GET:
        query = request.GET['q']
        context['query'] = str(query)
        return HttpResponseRedirect("/lists" %t.id)
    else:
        pass
    context['users'] = User.objects.filter(Q(username__icontains='o'))
    return context