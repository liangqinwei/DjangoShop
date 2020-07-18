from django.http import HttpResponse


# Create your views here.

def index(*args, **kwargs):
    return HttpResponse("<H1>This is my first DJango</H1>")
