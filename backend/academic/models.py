"""
Modelos relacionados con información académica.
"""
from django.db import models


class Docente(models.Model):
    """
    Docente universitario.
    """
    id_docente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    apellido = models.CharField(max_length=100, verbose_name="Apellido")
    nombre_completo = models.CharField(max_length=200, verbose_name="Nombre Completo", blank=True)
    alias_search = models.TextField(verbose_name="Alias Search", blank=True, help_text="Para búsquedas")
    
    def save(self, *args, **kwargs):
        if not self.nombre_completo:
            self.nombre_completo = f"{self.nombre} {self.apellido}".strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre_completo

    class Meta:
        verbose_name = "Docente"
        verbose_name_plural = "Docentes"


class Comision(models.Model):
    """
    Comisión de una cátedra (antes Catedra).
    """
    id_comision = models.AutoField(primary_key=True)
    # Campos principales
    codigo = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Código",
        help_text="Código único de la comisión"
    )
    nombre = models.CharField(
        max_length=200,
        verbose_name="Nombre"
    )
    
    # Docente titular/principal
    docente = models.ForeignKey(
        Docente,
        on_delete=models.CASCADE,
        related_name='comisiones',
        verbose_name="Docente",
        null=True, # Allow null for migration if needed, but ideally required
        blank=True
    )
    
    numero_catedra = models.IntegerField(
        null=True, 
        blank=True, 
        verbose_name="Número Cátedra"
    )
    
    horario = models.TextField(
        null=True,
        blank=True,
        verbose_name="Horario"
    )
    
    cuatrimestre = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Cuatrimestre"
    )
    
    # Información adicional mantenida
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
    objects: models.Manager['Comision']
    
    class Meta:
        verbose_name = "Comisión"
        verbose_name_plural = "Comisiones"
        ordering = ['codigo']
        indexes = [
            models.Index(fields=['codigo']),
            models.Index(fields=['activa']),
        ]
    
    def __str__(self) -> str:
        docente_str = str(self.docente) if self.docente else "Sin Docente"
        return f"{self.codigo} - {self.nombre} ({docente_str})"
