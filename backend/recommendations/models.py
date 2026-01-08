"""
Modelos para el sistema de recomendaciones.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
from django.conf import settings
from django.db import models

if TYPE_CHECKING:
    from academic.models import Comision
    from scraping.models import Post_Scrapeado, Sesion_Scraping
    from users.models import User


class Recomendacion(models.Model):
    """
    Recomendación de una cátedra.
    
    Extraída y procesada desde posts de Facebook usando NLP.
    """
    # Relaciones principales
    comision = models.ForeignKey(
        'academic.Comision',
        on_delete=models.CASCADE,
        related_name='recomendaciones',
        verbose_name="Comisión",
        null=True
    )
    post_origen = models.ForeignKey(
        'scraping.Post_Scrapeado',
        on_delete=models.CASCADE,
        related_name='recomendaciones',
        verbose_name="Post Origen"
    )
    contribuidor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contribuciones',
        verbose_name="Contribuidor",
        help_text="Usuario que contribuyó esta recomendación"
    )
    sesion_scraping = models.ForeignKey(
        'scraping.Sesion_Scraping',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recomendaciones',
        verbose_name="Sesión de Scraping"
    )
    
    # Contenido de la recomendación
    texto = models.TextField(
        verbose_name="Texto",
        help_text="Texto de la recomendación extraído del post"
    )
    sentimiento = models.CharField(
        max_length=50,
        choices=[
            ('positivo', 'Positivo'),
            ('negativo', 'Negativo'),
            ('neutral', 'Neutral'),
        ],
        default='neutral',
        verbose_name="Sentimiento",
        help_text="Análisis de sentimiento (positivo/negativo/neutral)"
    )
    confianza = models.FloatField(
        default=0.0,
        verbose_name="Confianza",
        help_text="Nivel de confianza del análisis NLP (0-1)"
    )
    
    # Nuevos campos del esquema
    prob_aprobar = models.CharField(
        max_length=50,
        choices=[
            ('alto', 'Alto'),
            ('medio', 'Medio'),
            ('bajo', 'Bajo'),
            ('desconocido', 'Desconocido'),
        ],
        default='desconocido',
        verbose_name="Probabilidad de Aprobar"
    )
    docent_perf = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Perfil Docente",
        help_text="Atributos extraídos del docente"
    )
    parciales_tipo = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Tipo de Parciales"
    )
    asistencia = models.BooleanField(
        default=False,
        verbose_name="Asistencia Obligatoria"
    )
    toma_tp = models.BooleanField(
        default=False,
        verbose_name="Toma TP"
    )
    
    # Votación comunitaria
    votos_utilidad = models.IntegerField(
        default=0,
        verbose_name="Votos de Utilidad",
        help_text="Cantidad de votos positivos de la comunidad"
    )
    
    # Timestamps
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación"
    )
    fecha_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de Modificación"
    )
    
    # Django ORM manager (explícito para type checking)
    objects: models.Manager['Recomendacion']
    
    class Meta:
        verbose_name = "Recomendación"
        verbose_name_plural = "Recomendaciones"
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['comision', '-fecha_creacion']),
            models.Index(fields=['sentimiento']),
            models.Index(fields=['-votos_utilidad']),
        ]
    
    def __str__(self) -> str:
        comision_codigo = self.comision.codigo if hasattr(self.comision, 'codigo') else str(self.comision)
        return f"{comision_codigo} - {self.sentimiento} ({self.confianza:.2f})"


class Cache_Metadatos(models.Model):
    """
    Control de versiones para cache del cliente.
    
    Permite que el cliente (extensión/web) sepa cuándo actualizar su cache local.
    """
    # Versión actual de los datos
    version = models.IntegerField(
        default=1,
        verbose_name="Versión",
        help_text="Versión actual del dataset"
    )
    
    # Última actualización
    ultima_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Actualización"
    )
    
    # Metadatos adicionales
    hash = models.CharField(
        max_length=64,
        blank=True,
        verbose_name="Hash",
        help_text="Hash MD5/SHA256 del dataset para verificación"
    )
    
    # Django ORM manager (explícito para type checking)
    objects: models.Manager['Cache_Metadatos']
    
    class Meta:
        verbose_name = "Cache de Metadatos"
        verbose_name_plural = "Cache de Metadatos"
    
    def __str__(self) -> str:
        return f"Versión {self.version} - {self.ultima_actualizacion}"
    
    @classmethod
    def get_current_version(cls) -> int:
        """Obtiene o crea la versión actual."""
        obj, _ = cls.objects.get_or_create(id=1)
        return obj.version
    
    @classmethod
    def increment_version(cls) -> int:
        """Incrementa la versión actual."""
        obj, _ = cls.objects.get_or_create(id=1)
        obj.version += 1
        obj.save()
        return obj.version

