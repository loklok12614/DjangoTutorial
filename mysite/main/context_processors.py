from django.contrib.auth.models import User
from django.db.models import Q


def add_variable_to_context(request):
    context = {}

    query = ""
    if request.GET:
        pass
        # if request.GET['q']:
        #     query = request.GET['q']
        #     context['query'] = str(query)
    context['users'] = User.objects.filter(Q(username__icontains='o'))
    return context