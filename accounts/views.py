from django.http.response import HttpResponse
from django.shortcuts import render


# Create your views here.
def register(request):
    return render(request, "accounts/register.html")


def login(request):
    return render(request,"accounts/signin.html")


def logout(request):
    return HttpResponse("logout page")