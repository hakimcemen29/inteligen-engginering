from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from .models import Projek
from .serializers import ProjekSerializer  # ✅ Tambahkan ini



import requests

API_ENDPOINT = 'http://127.0.0.1:5001/api/meaningful/'

def get_meaningful_data(request):
    data = []
    error_message = None

    # --- Tempel token Anda di sini ---
    # GANTI 'YOUR_ACTUAL_API_TOKEN_HERE' dengan token yang baru saja Anda dapatkan
    auth_token = '4a95bc1e9a186ef0eb530ea128768e4273326f05' # <--- Tempel token Anda di sini!

    # Pastikan token tersedia
    if auth_token:
        headers = {
            'Authorization': f'Token {auth_token}',
            'Accept': 'application/json'
        }
        try:
            response = requests.get(API_ENDPOINT, headers=headers)
            response.raise_for_status() # Akan memunculkan error untuk status 4xx/5xx

            if response.headers.get('Content-Type') == 'application/json':
                data = response.json()
            else:
                error_message = f"Respons API bukan JSON. Content-Type: {response.headers.get('Content-Type')}"
                print(f"DEBUG: Non-JSON response: {response.text}")

        except requests.exceptions.RequestException as e:
            error_message = f"Terjadi kesalahan saat mengambil data dari API: {e}"
            print(f"Error fetching data: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"API Response Status: {e.response.status_code}")
                print(f"API Response Body: {e.response.text}")
        except ValueError as e: # Tangkap kesalahan penguraian JSON
            error_message = f"Terjadi kesalahan saat mengurai respons JSON: {e}"
            print(f"Error decoding JSON: {e}")
    else:
        error_message = "Token autentikasi tidak tersedia."

    context = {
        'data': data,
        'error_message': error_message,
    }
    return render(request, 'integrasi.html', context)
    


from .forms import (
    RegisterForm, LoginForm, ProjekForm, MeaningfulForm,
    ExperienceForm, ImplementasiForm, BatasanForm,
    RelasiForm, PerencanaanForm
)
from .models import (
    Projek, Meaningful, Experience, Implementasi,
    Batasan, Relasi, Perencanaan
)

def get_projek_or_redirect(request):
    projek_id = request.GET.get('projek_id') or request.POST.get('projek_id')
    if not projek_id:
        return None, redirect('projek')
    projek = get_object_or_404(Projek, id=projek_id, user=request.user)
    return projek, None

# Autentikasi
def landing(request):
    return render(request, 'landing.html')

def registerPage(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Registrasi berhasil. Silakan login.")
        return redirect('login')
    return render(request, 'register.html', {'form': form})

def login_view(request):
    form = LoginForm(data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('home')
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

# Dashboard dan Projek
@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

@login_required
def projek_view(request):
    form = ProjekForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        projek = form.save(commit=False)
        projek.user = request.user
        projek.save()
        messages.success(request, "Projek berhasil ditambahkan.")
        return redirect('projek')
    projek_list = Projek.objects.filter(user=request.user)
    return render(request, 'projek.html', {'form': form, 'projek_list': projek_list})

@login_required
def delete_projek(request, id):
    projek = get_object_or_404(Projek, id=id, user=request.user)
    projek.delete()
    messages.success(request, "Projek berhasil dihapus.")
    return redirect('projek')

# Wizard Steps
@login_required
def meaningful_input(request):
    projek, redirect_response = get_projek_or_redirect(request)
    if redirect_response: return redirect_response

    obj, _ = Meaningful.objects.get_or_create(projek=projek)
    form = MeaningfulForm(request.POST or None, instance=obj)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(f'/experience/?projek_id={projek.id}')

    return render(request, 'meaningful.html', {'form': form, 'projek_terpilih': projek})

@login_required
def experience_input(request):
    projek, redirect_response = get_projek_or_redirect(request)
    if redirect_response: return redirect_response

    obj, _ = Experience.objects.get_or_create(projek=projek)
    form = ExperienceForm(request.POST or None, instance=obj)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(f'/implementasi/?projek_id={projek.id}')

    return render(request, 'experience.html', {'form': form, 'projek_terpilih': projek})

@login_required
def implementasi_view(request):
    projek, redirect_response = get_projek_or_redirect(request)
    if redirect_response: return redirect_response

    obj, _ = Implementasi.objects.get_or_create(projek=projek)
    form = ImplementasiForm(request.POST or None, instance=obj)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(f'/batasan/?projek_id={projek.id}')

    return render(request, 'implementasi.html', {'form': form, 'projek_terpilih': projek})

@login_required
def batasan_view(request):
    projek, redirect_response = get_projek_or_redirect(request)
    if redirect_response: return redirect_response

    obj, _ = Batasan.objects.get_or_create(projek=projek)
    form = BatasanForm(request.POST or None, instance=obj)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(f'/status/?projek_id={projek.id}')

    return render(request, 'batasan.html', {'form': form, 'projek_terpilih': projek})

@login_required
def statusRelasi_view(request):
    projek, redirect_response = get_projek_or_redirect(request)
    if redirect_response: return redirect_response

    obj, _ = Relasi.objects.get_or_create(projek=projek)
    form = RelasiForm(request.POST or None, instance=obj)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect(f'/perencanaan/?projek_id={projek.id}')

    return render(request, 'status.html', {'form': form, 'projek_terpilih': projek})

@login_required
def perencanaan_view(request):
    projek, redirect_response = get_projek_or_redirect(request)
    if redirect_response: return redirect_response

    obj, _ = Perencanaan.objects.get_or_create(projek=projek)
    form = PerencanaanForm(request.POST or None, instance=obj)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('projek')

    return render(request, 'perencanaan.html', {'form': form, 'projek_terpilih': projek})

# View Detail Projek
@login_required
def view_projek_detail(request, projek_id):
    projek = get_object_or_404(Projek, id=projek_id, user=request.user)
    context = {
        'projek': projek,
        'meaningful_list': Meaningful.objects.filter(projek=projek),
        'experience_list': Experience.objects.filter(projek=projek),
        'implementasi_list': Implementasi.objects.filter(projek=projek),
        'batasan_list': Batasan.objects.filter(projek=projek),
        'relasi_list': Relasi.objects.filter(projek=projek),
        'perencanaan_list': Perencanaan.objects.filter(projek=projek),
    }
    return render(request, 'viewProjek.html', context)

def profil_view(request):
    return render(request, 'profil.html')


def home_view(request):
    return render(request, 'home.html')

def view_tess(request):
    return render(request, 'tess.html')

@login_required
def projek_chart_data(request):
    projek_list = Projek.objects.filter(user=request.user).order_by('created_at')
    data = [
        {
            'tanggal': p.created_at.strftime('%Y-%m-%d'),
            'nama': p.nama,
        } for p in projek_list
    ]
    return JsonResponse(data, safe=False)




class ProjekAPIViewSet(viewsets.ModelViewSet):
    serializer_class = ProjekSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Projek.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not all([username, email, password]):
        return Response({'error': 'Semua field wajib diisi'}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username sudah digunakan'}, status=400)

    user = User.objects.create_user(username=username, email=email, password=password)
    token = Token.objects.create(user=user)
    return Response({'token': token.key})
