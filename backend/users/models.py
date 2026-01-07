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
    
    # Django ORM manager (explícito para type checking)
    objects: models.Manager['User']
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['-date_joined']
    
    def __str__(self) -> str:
        return f"{self.username} ({self.email})"
