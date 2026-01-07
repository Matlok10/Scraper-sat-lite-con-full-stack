"""
Modelos relacionados con información académica.
"""
from django.db import models


class Catedra(models.Model):
    """
    Cátedra universitaria.
    
    Representa una materia/cátedra sobre la cual se pueden hacer recomendaciones.
    Catálogo de ~500 cátedras.
    """
    # Campos principales
    codigo = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Código",
        help_text="Código único de la cátedra"
    )
    nombre = models.CharField(
        max_length=200,
        verbose_name="Nombre"
    )
    titular = models.CharField(
        max_length=200,
        verbose_name="Profesor Titular"
    )
    
    # Información adicional
    mencion_fb = models.IntegerField(
        default=0,
        verbose_name="Menciones en Facebook",
        help_text="Cantidad de veces mencionada en posts"
    )
    
    # Metadatos
    ano = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Año",
        help_text="Año de la carrera (1, 2, 3, etc.)"
    )
    
    # Timestamps
    ultima_actualizacion_scraping = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Actualización"
    )
    activa = models.BooleanField(
        default=True,
        verbose_name="Activa",
        help_text="Si la cátedra está activa actualmente"
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación"
    )
    
    # Django ORM manager (explícito para type checking)
    objects: models.Manager['Catedra']
    
    class Meta:
        verbose_name = "Cátedra"
        verbose_name_plural = "Cátedras"
        ordering = ['codigo']
        indexes = [
            models.Index(fields=['codigo']),
            models.Index(fields=['titular']),
            models.Index(fields=['activa']),
        ]
    
    def __str__(self) -> str:
        return f"{self.codigo} - {self.nombre} ({self.titular})"
