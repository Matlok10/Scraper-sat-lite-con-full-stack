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
    # Django ORM manager (explícito para type checking)
    objects: models.Manager['Docente']
    
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
    
    Nota importante: El código de comisión (ej: 0620, 0016) puede repetirse 
    si tiene diferentes horarios o docentes. El identificador único es 
    la combinación de: código + docente + horario + cuatrimestre
    """
    id_comision = models.AutoField(primary_key=True)
    # Campos principales
    codigo = models.CharField(
        max_length=50,
        verbose_name="Código",
        help_text="Código único de la comisión en el sistema de la facultad"
    )
    codigo_actividad = models.CharField(
        max_length=50,
        verbose_name="Código de Actividad",
        help_text="Código de la materia (ej: 205, 2X8, 73U, 85S)",
        blank=True,
        default=""
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

    sede = models.CharField(
        max_length=150,
        blank=True,
        default="",
        verbose_name="Sede u orientación",
        help_text="Orientación (General, Penal, Notarial) o nombre de la institución en centros externos"
    )

    es_centro_externo = models.BooleanField(
        default=False,
        verbose_name="Centro externo",
        help_text="Indica si la comisión corresponde a un centro externo"
    )

    CICLO_CHOICES = [
        ('CPO', 'Ciclo Profesional Orientado'),
        ('CPC', 'Ciclo Profesional Común'),
    ]

    ciclo = models.CharField(
        max_length=3,
        blank=True,
        default="",
        choices=CICLO_CHOICES,
        verbose_name="Ciclo (CPO/CPC)",
        help_text="Indica si pertenece al Ciclo Profesional Orientado (CPO) o Común (CPC)"
    )
    
    modalidad = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Modalidad",
        choices=[
            ('Presencial', 'Presencial'),
            ('Remota', 'Remota'),
            ('Híbrida', 'Híbrida'),
        ],
        help_text="Modalidad de dictado de la comisión"
    )
    
    cuatrimestre = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Cuatrimestre"
    )
    
    # ========================================================================
    # RECOMENDACIONES - Campos para absorber datos del CSV y procesar con scraper
    # ========================================================================
    
    recomendacion_raw = models.TextField(
        null=True,
        blank=True,
        verbose_name="Recomendación (texto original)",
        help_text="Texto original de la recomendación sin procesar"
    )
    
    # Campos estructurados que el scraper extraerá de recomendacion_raw
    tipo_catedra = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Tipo de Cátedra",
        choices=[
            ('recomendable', 'Cátedra Recomendable'),
            ('no_recomendable', 'Cátedra NO Recomendable'),
            ('exigente', 'Cátedra Exigente'),
            ('para_aprender', 'Cátedra para Aprender'),
            ('accesible', 'Cátedra Accesible'),
        ],
        help_text="Clasificación según probabilidad de aprobar"
    )
    
    toma_asistencia = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="Toma Asistencia",
        help_text="Si la cátedra toma asistencia o no"
    )
    
    tipo_parciales = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Tipo de Parciales",
        help_text="Descripción de los parciales (escrito, oral, MC, etc.)"
    )
    
    toma_trabajos_practicos = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="Toma Trabajos Prácticos",
        help_text="Si la cátedra da trabajos prácticos"
    )
    
    nivel_aprobados = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Nivel de Aprobados",
        choices=[
            ('alto', 'Alta tasa de aprobados'),
            ('medio', 'Tasa media de aprobados'),
            ('bajo', 'Baja tasa de aprobados'),
        ],
        help_text="Nivel de aprobación de estudiantes"
    )
    
    llegada_docente = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        verbose_name="Llegada del Docente",
        choices=[
            ('buena', 'Buena llegada a los estudiantes'),
            ('mala', 'Mala llegada a los estudiantes'),
            ('regular', 'Llegada regular'),
        ],
        help_text="Cómo es la relación docente-estudiante"
    )
    
    bibliografia_info = models.TextField(
        null=True,
        blank=True,
        verbose_name="Información de Bibliografía",
        help_text="Detalles sobre el material de estudio"
    )
    
    # Campo para el scraper: indica si ya fue procesada
    recomendacion_procesada = models.BooleanField(
        default=False,
        verbose_name="Recomendación Procesada",
        help_text="Indica si el scraper ya procesó la recomendación"
    )
    
    # ========================================================================
    # FIN RECOMENDACIONES
    # ========================================================================
    
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
        # El identificador único es la combinación de estos campos
        unique_together = [
            ['codigo', 'docente', 'horario', 'cuatrimestre', 'sede']
        ]
        indexes = [
            models.Index(fields=['codigo', 'cuatrimestre']),
            models.Index(fields=['docente', 'cuatrimestre']),
            models.Index(fields=['codigo_actividad']),
            models.Index(fields=['activa']),
            models.Index(fields=['sede']),
            models.Index(fields=['es_centro_externo']),
        ]
    
    def __str__(self) -> str:
        docente_str = str(self.docente) if self.docente else "Sin Docente"
        return f"{self.codigo} - {self.nombre} ({docente_str})"
