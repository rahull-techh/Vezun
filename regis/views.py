from django.shortcuts import render
from django.urls import path,include
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password 

# Create your views here.

def home(request):
    return JsonResponse({
        "message":"Welcome to Vezun",
        "user":str(request.user),
        "authenticated":request.user.is_authenticated,
    })

@csrf_exempt
def regis(request):

    if request.method == "GET":
        return render(request,"registration.html")

    if request.method != "POST":
        return JsonResponse({"error":"POST request required"},status=400)

    full_nm = request.POST.get("full_nm")
    username = request.POST.get("username")
    role = request.POST.get("role")
    password = request.POST.get("password")
    email = request.POST.get("email")

    if not full_nm or not username or not role or not password or not email :
        return JsonResponse({"error1":"All Fields are required"}, status = 400)

    if not('@' in password or '$' in password) and any(c.isdigit() for c in password) and any(c.isalpha() for c in password):
        return JsonResponse({"error2":"Create a strong password using @,$ and a combination of digits and alphabets"})

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({"error":"Please Enter a valid email"},status = 400)

    if User.objects.filter(username).exists:
        return JsonResponse({"error":"Username already exist use another username"},status=400)

    if User.objects.filter(email).exists:
        return JsonResponse({"error":"Email already registered"},status=400)

    hashed_pwd = make_password(password)

    user = User.objects.create(
        username = username,
        name = full_nm,
        password= hashed_pwd,
        is_active = False,
    )

    return JsonResponse({"message":"Registration Successfull"},status=200)