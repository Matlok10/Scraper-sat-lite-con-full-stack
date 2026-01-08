"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from pathlib import Path

from django.conf import settings
from django.contrib import admin
from django.http import HttpResponse, HttpResponseNotFound
from django.urls import path, re_path, include
from django.views.static import serve
from rest_framework.routers import DefaultRouter

from academic.views import ComisionViewSet
from scraping.views import (
    GruposViewSet, TareaScrapeoViewSet, 
    SesionScrapingViewSet, PostScrapeadoViewSet
)
from users.views import UserLoginView, UserLogoutView, UserViewSet

# API Router configuration
router = DefaultRouter()
router.register(r'catedras', ComisionViewSet, basename='catedra')
router.register(r'grupos', GruposViewSet, basename='grupo')
router.register(r'tareas', TareaScrapeoViewSet, basename='tarea')
router.register(r'sesiones', SesionScrapingViewSet, basename='sesion')
router.register(r'posts', PostScrapeadoViewSet, basename='post')
router.register(r'users', UserViewSet, basename='user')


def spa_view(request):
    """Serve the compiled frontend index.html."""
    index_path = Path(settings.BASE_DIR) / 'static' / 'frontend' / 'index.html'
    if not index_path.exists():
        return HttpResponseNotFound("Frontend build not found. Run 'npm run build' in frontend.")
    content = index_path.read_text(encoding='utf-8')
    return HttpResponse(content)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/login/', UserLoginView.as_view(), name='login'),
    path('api/auth/logout/', UserLogoutView.as_view(), name='logout'),
]

# Serve static files in development (MUST be before catch-all)
if settings.DEBUG:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, {
            'document_root': settings.BASE_DIR / 'static'
        }),
        re_path(r'^assets/(?P<path>.*)$', serve, {
            'document_root': settings.BASE_DIR / 'static' / 'frontend' / 'assets'
        }),
    ]

# SPA catch-all (MUST be last)
urlpatterns += [
    re_path(r'^.*$', spa_view, name='spa'),
]

