"""
Configuración del panel de administración para la app users.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin personalizado para el modelo User."""
    
    list_display = ['username', 'email', 'rol', 'puntos', 'contribuciones_aprobadas', 'is_staff', 'date_joined']
    list_filter = ['rol', 'is_staff', 'is_superuser', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    # Agregar campos personalizados a los fieldsets
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Información Adicional', {
            'fields': ('rol', 'puntos', 'contribuciones_aprobadas', 'puede_scrapear', 'sesiones_scraping_activas')
        }),
    )
