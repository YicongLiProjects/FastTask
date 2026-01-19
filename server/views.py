from django.shortcuts import render

def signup(request):
    return render(request, 'signUpPage.html')

def login(request):
    return render(request, 'loginPage.html')

def password_reset_email(request):
    return render(request, 'passwordResetEmailPage.html')

def app_home(request):
    return render(request, 'mainPage.html')

def app(request):
    return render(request, 'appPage.html')