import json
import os
import sys
from pathlib import Path

import boto3

import config.settings

sys.path.append(Path(__file__).resolve().parent.parent.__str__())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

import django
django.setup()

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from datetime import datetime
from .models import *
from django.middleware.csrf import get_token
from django.shortcuts import render


# @ marks the start of a decorator used to support various HTTP features

# Server scripting logic
@csrf_exempt
def signup(request):
    # Edge cases with HTTP requests
    # Use POST request for sensitive user information handling
    # The error code 400 means a bad request has been sent
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)
    try:
        data = json.loads(request.body)
    except json.decoder.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    display_name = data.get("display_name", "").strip()
    password = data.get("password", "").strip()
    email = data.get("email", "").strip()
    first_name = data.get("first_name", "").strip()
    last_name = data.get("last_name", "").strip()
    dob = data.get("dob", "").strip()
    dob_format = "%Y-%m-%d"
    try:
        dob = datetime.strptime(dob, dob_format).date()
    except ValueError:
        # 1 January 1900 is the default date of birth if no input is provided
        dob = datetime.strptime("1900-01-01", dob_format).date()

    # Check if the user already exists
    if Profile.objects.filter(user__email=email).exists():
        return JsonResponse({"error": "This email is already registered"}, status=409)

    # Input verification
    if not display_name or not password or not email:
        return JsonResponse({"error": "Missing required fields"}, status=400)
    if len(display_name) > 20:
        return JsonResponse({"error": "Username too long"}, status=400)
    if dob is not None and dob > timezone.localdate():
        return JsonResponse({"error": "Date of birth must be before now"}, status=400)
    if len(first_name) > 30 or len(last_name) > 30:
        return JsonResponse({"error": "Name must be under 30 characters"}, status=400)
    if len(password) < 8 or len(password) > 20:
        return JsonResponse({"error": "Password must be between 8 and 20 characters"}, status=400)

    user = User.objects.create_user(email, email, password, first_name=first_name, last_name=last_name)
    profile = Profile(user=user, dob=dob, xp=0, level=1, pfp=None, display_name=display_name)
    profile.save()

    return JsonResponse({"status": "ok", 'csrfToken': get_token(request)}, status=201)


@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)
    try:
        data = json.loads(request.body)
    except json.decoder.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    if not Profile.objects.filter(user__username=email).exists():
        return JsonResponse({"error": "This user does not exist yet. Please create a new account"}, status=409)

    user = authenticate(username=email, password=password)
    if user is None:
        return JsonResponse({"error": "Invalid credentials"}, status=401)
    login(request, user)
    return JsonResponse({"status": "ok"}, status=200)


def logout_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)
    logout(request)
    return JsonResponse({"status": "ok"}, status=200)


@login_required
def get_profile(request):
    # Use GET request to retrieve information
    if request.method != "GET":
        return JsonResponse({"error": "GET request required"}, status=400)
    profile = request.user.profile
    return JsonResponse({
        "username": profile.user.username,
        "dob": profile.dob,
        "xp": profile.xp,
        "level": profile.level,
        "pfp_url": profile.pfp_url
    })


@csrf_exempt
@login_required
def update_profile(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)

    # Get fields to update
    fn = request.POST.get("first_name", "").strip()
    ln = request.POST.get("last_name", "").strip()
    dob = request.POST.get("dob", "").strip()
    email = request.POST.get("email", "").strip()
    display_name = request.POST.get("display_name", "").strip()
    password = request.POST.get("password", "").strip()
    pfp = request.FILES.get("pfp")

    dob_format = "%Y-%m-%d"
    try:
        dob = datetime.strptime(dob, dob_format).date()
    except ValueError:
        # 1 January 1900 is the default date of birth if no input is provided
        dob = datetime.strptime("1900-01-01", dob_format).date()

    # Get profile to update defined by user ID to ensure state consistency
    profile = Profile.objects.get(user_id=request.user.id)

    # Delete old file
    if profile.pfp:
        profile.pfp.delete(save=False)

    # Check file format
    if pfp is not None and pfp.content_type not in ["image/png", "image/jpg", "image/jpeg"]:
        return JsonResponse({"error": "Invalid file extension"}, status=400)

    if fn is not None and fn != "" and len(fn) <= 30:
        profile.user.first_name = fn

    if ln is not None and ln != "" and len(ln) <= 30:
        profile.user.last_name = ln

    if password is not None and password != "" and 8 <= len(password) <= 20:
        profile.user.set_password(password)

    if email is not None and email != "":
        profile.user.email = email
        profile.user.username = email

    if dob is not None and dob != "":
        profile.dob = dob

    if display_name is not None and display_name != "" and len(display_name) <= 20:
        profile.display_name = display_name

    if pfp is not None:
        profile.pfp = pfp

    profile.user.save()
    profile.save()

    return JsonResponse({"status": "ok"}, status=200)


@login_required
def get_tasks(request):
    if request.method != "GET":
        return JsonResponse({"error": "GET request required"}, status=400)

    tasks = request.GET.get("tasks", "")
    return JsonResponse(tasks, status=200)


@csrf_exempt
@login_required
def add_task(request):
    pass


@csrf_exempt
@login_required
def remove_task(request):
    pass


@csrf_exempt
@login_required
def edit_task(request):
    pass


# HTML page views
def index(request):
    return render(request, 'index.html')

def signup_view(request):
    return render(request, 'signUpPage.html')

def login_view(request):
    return render(request, 'loginPage.html')

@login_required
def app_view(request):
    return render(request, 'appPage.html')

@login_required
def account_info_view(request):
    return render(request, 'accountInfoPage.html')

def password_reset_email_view(request):
    return render(request, 'passwordResetEmailPage.html')

def help_view(request):
    return render(request, 'helpPage.html')
