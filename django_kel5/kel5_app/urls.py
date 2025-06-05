from django.urls import path
from . import views
from .views import registerPage, login_view, dashboard_view, logout_view,maeningful_view,experience_view,implementasi_view,batasan_view,statusRelasi_view,perencanaan_view,profil_view,projek_view,home_view

urlpatterns = [
    path('', views.landing, name='landing'),
    path('login/',views.login_view,name='login'),
    path('register/',views.registerPage,name='registerPage'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    path('maeningful/',maeningful_view,name='maeningful'),
    path('experience/',experience_view,name='experience'),
    path('batasan/',batasan_view,name='batasan'),
    path('perencanaan/',perencanaan_view,name='perencanaan'),
    path('status/',statusRelasi_view,name='status'),
    path('profil/',profil_view,name='profil'),
    path('projek/',projek_view,name='projek'),
    path('implementasi/',implementasi_view,name='implementasi'),
    path('home/',home_view,name='home')
]
