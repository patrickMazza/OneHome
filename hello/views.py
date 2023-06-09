import re
from django.utils.timezone import datetime
from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return HttpResponse("Hello, Django!")


def hello_there(request, name):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! It's " + formatted_now
    return HttpResponse(content)


def index(request):
    return HttpResponse('<h1>My blog</h1>')


def base(request):

    # render function takes argument  - request
    # and return HTML as response
    return render(request, "hello/base.html")


def greet(request, name):
    return HttpResponse(f"Hello, {name.capitalize()}!")


def about(request):
    return HttpResponse('<h1>About</h1>')
