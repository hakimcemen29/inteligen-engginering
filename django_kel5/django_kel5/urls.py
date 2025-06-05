from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('kel5_app.urls')),  # FIXED: removed extra comma
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
