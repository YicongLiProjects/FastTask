import json
import os
import sys
from pathlib import Path
sys.path.append(Path(__file__).resolve().parent.parent.__str__())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

import django
django.setup()

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.utils import timezone
from .models import *
from django.middleware.csrf import get_token


# @ marks the start of a decorator used to support various HTTP features

@csrf_exempt
def signup(request):
    # Edge cases with HTTP requests
    # Use POST request for sensitive user information handling
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)
    try:
        data = json.loads(request.body)
    except json.decoder.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    email = data.get("email", "").strip()
    first_name = data.get("first_name", "").strip()
    last_name = data.get("last_name", "").strip()
    dob = data.get("dob", "").strip()

    # Input verification
    if not username or not password or not email:
        return JsonResponse({"error": "Missing required fields"}, status=400)
    if len(username) > 20:
        return JsonResponse({"error": "Username too long"}, status=400)
    if dob is not None and timezone.localdate() < dob:
        return JsonResponse({"error": "Date of birth must be before now"}, status=400)
    if User.objects.filter(email=email).exists():
        return JsonResponse({"error": "This email is already registered"}, status=400)
    if len(first_name) > 30 or len(last_name) > 30:
        return JsonResponse({"error": "Name must be under 30 characters"}, status=400)


    user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
    profile = Profile(user=user, dob=dob, xp=0, level=1, pfp=None)
    profile.save()

    return JsonResponse({"status": "ok", 'csrfToken': get_token(request)})


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

    user = authenticate(email=email, password=password)
    if user is None:
        return JsonResponse({"error": "Invalid credentials"}, status=400)
    login(request, user)
    return JsonResponse({"status": "ok"})


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
    fn = request.POST.get("first_name", "")
    ln = request.POST.get("last_name", "")
    dob = request.POST.get("dob", "")
    email = request.POST.get("email", "")
    username = request.POST.get("username", "")
    password = request.POST.get("password", "")
    pfp = request.POST.get("pfp", "")
    user = User.objects.create_user(username, email, password, first_name=fn, last_name=ln)
    profile = Profile.objects.get(user=user)
    profile.dob = dob
    profile.pfp = pfp
    return None


@login_required
def get_task(request):
    pass


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