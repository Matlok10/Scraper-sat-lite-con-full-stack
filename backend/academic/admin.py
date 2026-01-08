"""
Configuración del panel de administración para la app academic.
"""
from django.contrib import admin
from .models import Comision, Docente


@admin.register(Comision)
class ComisionAdmin(admin.ModelAdmin):
    """Admin para el modelo Comisión."""
    
    list_display = ['codigo', 'nombre', 'docente', 'ano', 'mencion_fb', 'activa', 'fecha_creacion']
    list_filter = ['activa', 'ano', 'ultima_actualizacion_scraping']
    search_fields = ['codigo', 'nombre', 'docente__nombre', 'docente__apellido']
    ordering = ['codigo']
    
    fieldsets = (
        ('Información Principal', {
            'fields': ('codigo', 'nombre', 'docente', 'ano', 'numero_catedra', 'horario', 'cuatrimestre')
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


@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    """Admin para el modelo Docente."""
    list_display = ('nombre_completo', 'nombre', 'apellido')
    search_fields = ('nombre', 'apellido', 'alias_search')
