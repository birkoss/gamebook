from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


def home(request):
    return render(request, "core/home.html")

def user_login(request):
    return render(request, "core/login.html")

@login_required
def user_logout(request):
	logout(request)
	return redirect('home')
