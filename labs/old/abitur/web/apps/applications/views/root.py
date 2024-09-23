from django.http import HttpRequest, HttpResponse


def root(request):
    return HttpResponse("ok", 200)
