"""
Configuración del panel de administración para la app recommendations.
"""
from django.contrib import admin
from .models import Recomendacion, Cache_Metadatos


@admin.register(Recomendacion)
class RecomendacionAdmin(admin.ModelAdmin):
    """Admin para el modelo Recomendacion."""
    
    list_display = ['id', 'comision', 'sentimiento', 'confianza', 'votos_utilidad', 'contribuidor', 'fecha_creacion']
    list_filter = ['sentimiento', 'fecha_creacion', 'comision']
    search_fields = ['texto', 'comision__codigo', 'comision__nombre', 'contribuidor__username']
    ordering = ['-fecha_creacion']
    
    readonly_fields = ['fecha_creacion', 'fecha_modificacion']
    
    fieldsets = (
        ('Información Principal', {
            'fields': ('comision', 'texto', 'sentimiento', 'confianza', 'prob_aprobar', 'docent_perf', 'parciales_tipo', 'asistencia', 'toma_tp')
        }),
        ('Relaciones', {
            'fields': ('post_origen', 'contribuidor', 'sesion_scraping')
        }),
        ('Votación', {
            'fields': ('votos_utilidad',)
        }),
        ('Metadatos', {
            'fields': ('fecha_creacion', 'fecha_modificacion'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Cache_Metadatos)
class CacheMetadatosAdmin(admin.ModelAdmin):
    """Admin para el modelo Cache_Metadatos."""
    
    list_display = ['id', 'version', 'ultima_actualizacion', 'hash']
    readonly_fields = ['ultima_actualizacion']
    
    def has_add_permission(self, request):
        """Solo puede haber un registro de cache."""
        return Cache_Metadatos.objects.count() == 0  # type: ignore[misc]
    
    def has_delete_permission(self, request, obj=None):
        """No se puede eliminar el registro de cache."""
        return False
