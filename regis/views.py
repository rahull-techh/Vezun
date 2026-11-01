from django.shortcuts import render
from django.urls import path,include
from django.http import JsonResponse


# Create your views here.
def regis(request):

    if request.method != "POST":
        return JsonResponse()
