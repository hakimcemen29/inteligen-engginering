from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def landing(request):
    return render(request, 'landing.html')


def registerPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            return render(request, 'register.html', {'error_message': 'Password tidak cocok!'})

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error_message': 'Username sudah digunakan!'})

        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {'error_message': 'Email sudah digunakan!'})

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        return redirect('login')

    return render(request, 'register.html')
def login_view(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # ganti dengan url dashboard kamu
        else:
            error_message = "Username atau password salah!"

    return render(request, 'login.html', {'error_message': error_message})


@login_required(login_url='login')
def dashboard_view(request):
    return render(request, 'dashboard.html', {'user': request.user})

def logout_view(request):
    logout(request)
    return redirect('login')

def maeningful_view(request):
    return render(request, 'maeningful.html')

def experience_view(request):
    return render(request, 'experience.html')

def implementasi_view(request):
    return render(request, 'implementasi.html')

def batasan_view(request):
    return render(request, 'batasan.html')

def perencanaan_view(request):
    return render(request, 'perencanaan.html')

def statusRelasi_view(request):
    return render(request, 'status.html')

def profil_view(request):
    return render(request, 'profil.html')

def projek_view(request):
    return render(request, 'projek.html')


def home_view(request):
    return render(request, 'home.html')

