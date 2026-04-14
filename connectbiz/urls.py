from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.usuarios.urls')),
    path('', include('apps.empresas.urls')),
    path('', include('apps.publicacoes.urls')),
    path('', include('apps.avaliacoes.urls')),
    path('', include('apps.relatorios.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
