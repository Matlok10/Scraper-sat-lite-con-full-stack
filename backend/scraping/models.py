"""
Modelos para el sistema de scraping colaborativo.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
from django.conf import settings
from django.db import models

if TYPE_CHECKING:
    from users.models import User


class Grupos(models.Model):
    """
    Grupos de Facebook a scrapear.
    
    Define los grupos públicos de Facebook donde se buscarán recomendaciones.
    """
    # Identificación del grupo
    nombre = models.CharField(
        max_length=200,
        verbose_name="Nombre del Grupo"
    )
    url = models.URLField(
        unique=True,
        verbose_name="URL",
        help_text="URL del grupo de Facebook"
    )
    
    # Estado
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    prioridad = models.IntegerField(
        default=0,
        verbose_name="Prioridad",
        help_text="Mayor prioridad = se scrapea más frecuentemente"
    )
    
    # Timestamps
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación"
    )
    ultima_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Actualización"
    )
    
    # Django ORM manager (explícito para type checking)
    objects: models.Manager['Grupos']
    
    class Meta:
        verbose_name = "Grupo"
        verbose_name_plural = "Grupos"
        ordering = ['-prioridad', 'nombre']
    
    def __str__(self) -> str:
        return self.nombre  # type: ignore[return-value]


class Tarea_Scrapeo(models.Model):
    """
    Tareas de scraping pendientes.
    
    Define QUÉ debe scrapearse. El backend crea estas tareas,
    la extensión del navegador las ejecuta.
    """
    # Relación con grupo
    grupo = models.ForeignKey(
        Grupos,
        on_delete=models.CASCADE,
        related_name='tareas',
        verbose_name="Grupo"
    )
    
    # Keywords a buscar
    keywords = models.JSONField(
        verbose_name="Palabras Clave",
        help_text="Lista de keywords para buscar en el grupo"
    )
    
    # Estado de la tarea
    busquedas_pendientes = models.JSONField(
        verbose_name="Búsquedas Pendientes",
        help_text="Keywords que aún no han sido procesados"
    )
    
    # Frecuencia
    frecuencia = models.CharField(
        max_length=50,
        default='semanal',
        verbose_name="Frecuencia",
        help_text="Qué tan seguido actualizar (diaria, semanal, mensual)"
    )
    
    # Control de ejecución
    posts_encontrados = models.IntegerField(
        default=0,
        verbose_name="Posts Encontrados"
    )
    
    activa = models.BooleanField(
        default=True,
        verbose_name="Activa",
        help_text="Si la tarea está habilitada para ejecutarse"
    )
    
    # Timestamps
    ultima_ejecucion = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Última Ejecución"
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación"
    )
    
    # Django ORM manager (explícito para type checking)
    objects: models.Manager['Tarea_Scrapeo']
    
    class Meta:
        verbose_name = "Tarea de Scraping"
        verbose_name_plural = "Tareas de Scraping"
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['grupo', '-fecha_creacion']),
        ]
    
    def __str__(self) -> str:
        grupo_nombre = self.grupo.nombre if hasattr(self.grupo, 'nombre') else str(self.grupo)
        return f"Tarea {self.pk} - {grupo_nombre}"


class Sesion_Scraping(models.Model):
    """
    Registro de sesiones de scraping por usuario.
    
    Cada vez que un usuario ejecuta tareas de scraping, se registra aquí.
    """
    # Relaciones
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sesiones_scraping',
        verbose_name="Usuario"
    )
    tarea = models.ForeignKey(
        Tarea_Scrapeo,
        on_delete=models.CASCADE,
        related_name='sesiones',
        verbose_name="Tarea"
    )
    
    # Información de la sesión
    estado = models.CharField(
        max_length=50,
        choices=[
            ('iniciado', 'Iniciado'),
            ('en_progreso', 'En Progreso'),
            ('completado', 'Completado'),
            ('error', 'Error'),
        ],
        default='iniciado',
        verbose_name="Estado"
    )
    
    # Timestamps
    inicio = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Inicio"
    )
    fin = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fin"
    )
    
    # Metadatos
    keywords_procesadas = models.JSONField(
        default=list,
        verbose_name="Keywords Procesadas",
        help_text="Lista de keywords que se procesaron en esta sesión"
    )
    posts_encontrados = models.IntegerField(
        default=0,
        verbose_name="Posts Encontrados"
    )
    recomendaciones_nuevas = models.IntegerField(
        default=0,
        verbose_name="Recomendaciones Nuevas"
    )
    
    # Django ORM manager (explícito para type checking)
    objects: models.Manager['Sesion_Scraping']
    
    class Meta:
        verbose_name = "Sesión de Scraping"
        verbose_name_plural = "Sesiones de Scraping"
        ordering = ['-inicio']
        indexes = [
            models.Index(fields=['usuario', '-inicio']),
            models.Index(fields=['estado']),
        ]
    
    def __str__(self) -> str:
        usuario_username = self.usuario.username if hasattr(self.usuario, 'username') else str(self.usuario)
        return f"Sesión {self.pk} - {usuario_username} - {self.estado}"


class Post_Scrapeado(models.Model):
    """
    Posts extraídos de Facebook.
    
    Almacena el contenido de los posts encontrados durante el scraping.
    El Post_id único evita duplicados.
    """
    # Identificación única del post
    post_id = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="ID del Post",
        help_text="Identificador único del post en Facebook"
    )
    
    # Relaciones
    grupo = models.ForeignKey(
        Grupos,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name="Grupo"
    )
    sesion_scraping = models.ForeignKey(
        Sesion_Scraping,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts',
        verbose_name="Sesión de Scraping"
    )
    
    # Contenido del post
    texto = models.TextField(
        verbose_name="Texto del Post"
    )
    autor = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Autor",
        help_text="Nombre del autor (anonimizado si es necesario)"
    )
    
    # Estado de procesamiento
    procesado = models.BooleanField(
        default=False,
        verbose_name="Procesado",
        help_text="Si ya se procesó con NLP para extraer recomendaciones"
    )
    
    # Timestamps
    fecha_post = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha del Post"
    )
    fecha_scraping = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Scraping"
    )
    
    # Django ORM manager (explícito para type checking)
    objects: models.Manager['Post_Scrapeado']
    
    class Meta:
        verbose_name = "Post Scrapeado"
        verbose_name_plural = "Posts Scrapeados"
        ordering = ['-fecha_scraping']
        indexes = [
            models.Index(fields=['post_id']),
            models.Index(fields=['procesado']),
            models.Index(fields=['grupo', '-fecha_scraping']),
        ]
    
    def __str__(self) -> str:
        post_id_short = self.post_id[:20] if len(self.post_id) > 20 else self.post_id  # type: ignore[misc]
        grupo_nombre = self.grupo.nombre if hasattr(self.grupo, 'nombre') else str(self.grupo)
        return f"Post {post_id_short}... - {grupo_nombre}"
