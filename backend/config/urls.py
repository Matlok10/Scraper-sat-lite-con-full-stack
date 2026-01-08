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
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from rest_framework.routers import DefaultRouter

from academic.views import DocenteViewSet, ComisionViewSet
from scraping.views import (
    GruposViewSet, TareaScrapeoViewSet, 
    SesionScrapingViewSet, PostScrapeadoViewSet
)
from users.views import UserViewSet, UserLoginView, UserLogoutView
from config.views import DashboardView, CatedrasView, RecommendationsView, ScrapingView, HistoryView

# API Router configuration
router = DefaultRouter()
router.register(r'docentes', DocenteViewSet, basename='docente')
router.register(r'catedras', ComisionViewSet, basename='catedra')
router.register(r'grupos', GruposViewSet, basename='grupo')
router.register(r'tareas', TareaScrapeoViewSet, basename='tarea')
router.register(r'sesiones', SesionScrapingViewSet, basename='sesion')
router.register(r'posts', PostScrapeadoViewSet, basename='post')
router.register(r'users', UserViewSet, basename='user')


def spa_view(_request):
    """Fallback view - redirect to dashboard"""
    from django.shortcuts import redirect
    return redirect('dashboard')


# URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    # Auth API endpoints (token-based)
    path('api/auth/login/', UserLoginView.as_view(), name='api-login'),
    path('api/auth/logout/', UserLogoutView.as_view(), name='api-logout'),

    # Template routes
    path('', DashboardView.as_view(), name='dashboard'),
    path('catedras/', CatedrasView.as_view(), name='catedras'),
    path('recomendaciones/', RecommendationsView.as_view(), name='recommendations'),
    path('scraping/', ScrapingView.as_view(), name='scraping'),
    path('historial/', HistoryView.as_view(), name='history'),
]

# Serve static files in development (MUST be before catch-all)
if settings.DEBUG:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, {
            'document_root': settings.BASE_DIR / 'static'
        }),
    ]

# SPA catch-all (MUST be last) - for API and undefined routes
urlpatterns += [
    re_path(r'^.*$', spa_view, name='spa'),
]

