from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages


def index(request):
    return render(request, 'login_app/index.html')


def login(request):
    response = User.objects.basicvalidator(request.POST, "Login")
    if type(response) == list:
        for error in response:
            messages.error(request, error)
        return redirect('/')
    request.session['user_id'] = response.id
    messages.success(request, "Logged In!")
    return redirect('/loggedin')


def register(request):
    response = User.objects.basicvalidator(request.POST, "Register")
    if type(response) == list:
        for error in response:
            messages.error(request, error)
        return redirect('/')
    request.session['user_id'] = response.id
    messages.success(request, "Registration Complete!")
    return redirect('/')


def logged(request):
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')
    context = {
        "loggeduser": User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'login_app/loggedin.html', context)
