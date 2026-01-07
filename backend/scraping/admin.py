"""
Configuración del panel de administración para la app scraping.
"""
from django.contrib import admin
from .models import Grupos, Tarea_Scrapeo, Sesion_Scraping, Post_Scrapeado


@admin.register(Grupos)
class GruposAdmin(admin.ModelAdmin):
    """Admin para el modelo Grupos."""
    
    list_display = ['nombre', 'url', 'activo', 'prioridad', 'fecha_creacion']
    list_filter = ['activo', 'prioridad']
    search_fields = ['nombre', 'url']
    ordering = ['-prioridad', 'nombre']


@admin.register(Tarea_Scrapeo)
class TareaScrapeoAdmin(admin.ModelAdmin):
    """Admin para el modelo Tarea_Scrapeo."""
    
    list_display = ['id', 'grupo', 'frecuencia', 'posts_encontrados', 'ultima_ejecucion', 'fecha_creacion']
    list_filter = ['frecuencia', 'ultima_ejecucion', 'grupo']
    search_fields = ['grupo__nombre']
    ordering = ['-fecha_creacion']
    
    readonly_fields = ['fecha_creacion']


@admin.register(Sesion_Scraping)
class SesionScrapingAdmin(admin.ModelAdmin):
    """Admin para el modelo Sesion_Scraping."""
    
    list_display = ['id', 'usuario', 'tarea', 'estado', 'posts_encontrados', 'recomendaciones_nuevas', 'inicio', 'fin']
    list_filter = ['estado', 'inicio']
    search_fields = ['usuario__username', 'tarea__grupo__nombre']
    ordering = ['-inicio']
    
    readonly_fields = ['inicio']


@admin.register(Post_Scrapeado)
class PostScrapeadoAdmin(admin.ModelAdmin):
    """Admin para el modelo Post_Scrapeado."""
    
    list_display = ['post_id_short', 'grupo', 'autor', 'procesado', 'fecha_post', 'fecha_scraping']
    list_filter = ['procesado', 'grupo', 'fecha_scraping']
    search_fields = ['post_id', 'texto', 'autor']
    ordering = ['-fecha_scraping']
    
    readonly_fields = ['fecha_scraping']
    
    def post_id_short(self, obj):
        """Muestra solo los primeros 20 caracteres del post_id."""
        return f"{obj.post_id[:20]}..."
    post_id_short.short_description = 'Post ID'
