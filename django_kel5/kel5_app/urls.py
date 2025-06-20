from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from .views import ProjekAPIViewSet, register_user  # ← ini yang penting

# Router untuk API projek
router = DefaultRouter()
router.register(r'projek', ProjekAPIViewSet, basename='projek-api')

urlpatterns = [
    # Autentikasi dan Navigasi
    path('', views.landing, name='landing'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Projek Web View
    path('projek/', views.projek_view, name='projek'),
    path('projek/delete/<int:id>/', views.delete_projek, name='delete_projek'),
    path('projek/detail/<int:projek_id>/', views.view_projek_detail, name='view_projek_detail'),

    # Wizard Step Views
    path('meaningful/', views.meaningful_input, name='meaningful'),
    path('experience/', views.experience_input, name='experience'),
    path('implementasi/', views.implementasi_view, name='implementasi'),
    path('batasan/', views.batasan_view, name='batasan'),
    path('status/', views.statusRelasi_view, name='status'),
    path('perencanaan/', views.perencanaan_view, name='perencanaan'),

    # Grafik dan Profil
    path('profil/', views.profil_view, name='profil'),
    path('home/', views.home_view, name='home'),
    path('tess/', views.view_tess, name='tess'),
    path('projek/chart-data/', views.projek_chart_data, name='projek_chart_data'),

    # Integrasi data eksternal
    path('integrasi/', views.get_meaningful_data, name='integrasi'),

    # API untuk Android
    path('api/', include(router.urls)),                  # GET/POST projek
    path('api/register/', register_user, name='api-register'),  # Register user Android
    path('api/login/', obtain_auth_token, name='api_login'),    # Login dan dapatkan token
]
