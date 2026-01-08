"""
Modelos de usuario para el sistema de recomendaciones.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Usuario extendido del sistema.
    
    Hereda de AbstractUser para tener todos los campos estándar:
    - username, email, password
    - first_name, last_name
    - is_active, is_staff, is_superuser
    """
    
    # Roles de usuario
    ROL_CHOICES = [
        ('estudiante', 'Estudiante'),
        ('colaborador', 'Colaborador Scraping'),
        ('moderador', 'Moderador'),
        ('admin', 'Administrador'),
    ]
    
    rol = models.CharField(
        max_length=20,
        choices=ROL_CHOICES,
        default='estudiante',
        verbose_name="Rol"
    )
    
    # Gamificación
    puntos = models.IntegerField(default=0, verbose_name="Puntos")
    contribuciones_aprobadas = models.IntegerField(default=0)
    
    # Metadata del scraper
    puede_scrapear = models.BooleanField(default=False)
    sesiones_scraping_activas = models.IntegerField(default=0)
    
    # Django ORM manager (explícito para type checking)
    objects: models.Manager['User']
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['-date_joined']
    
    def __str__(self) -> str:
        return f"{self.username} ({self.email}) - {self.rol}"
