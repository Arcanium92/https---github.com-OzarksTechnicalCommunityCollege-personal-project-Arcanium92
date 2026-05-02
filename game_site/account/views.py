from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('game_review:dashboard')

    return render(request, 'account/login.html')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('account:login')
    else:
        form = RegisterForm()

    return render(request, 'account/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return render(request, 'account/logout.html')