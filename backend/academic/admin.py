"""
Configuración del panel de administración para la app academic.
"""
from django.contrib import admin
from .models import Catedra


@admin.register(Catedra)
class CatedraAdmin(admin.ModelAdmin):
    """Admin para el modelo Catedra."""
    
    list_display = ['codigo', 'nombre', 'titular', 'ano', 'mencion_fb', 'activa', 'fecha_creacion']
    list_filter = ['activa', 'ano', 'ultima_actualizacion_scraping']
    search_fields = ['codigo', 'nombre', 'titular']
    ordering = ['codigo']
    
    fieldsets = (
        ('Información Principal', {
            'fields': ('codigo', 'nombre', 'titular', 'ano')
        }),
        ('Estado', {
            'fields': ('activa', 'mencion_fb')
        }),
        ('Metadatos', {
            'fields': ('ultima_actualizacion_scraping', 'fecha_creacion'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['ultima_actualizacion_scraping', 'fecha_creacion']
