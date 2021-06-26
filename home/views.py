from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm


def index(request):
    return render(request, 'home/index.html')


def register(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Log out before creating new account.')
        return redirect('home:index')

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account successfully created!')
            return redirect('home:index')
    context = {'form': form}
    return render(request, 'home/register.html', context)


def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logged out.')
    return redirect('home:index')


def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, 'Log out before logging in.')
        return redirect('home:index')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in!')
            return redirect('home:index')
        else:
            messages.warning(request, 'Username and/or password is incorrect, try again.')
            return redirect('home:login')
    else:
        return render(request, 'home/login.html')

