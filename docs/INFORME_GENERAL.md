# Informe General del Proyecto: Recos Completo

**Fecha**: 07 de Enero de 2026
**Estado**: En Desarrollo Activo

## 1. Resumen Ejecutivo

El proyecto "Recos Completo" es una plataforma web para la gestión y visualización de recomendaciones de cátedras universitarias. Permite a los usuarios ver comisiones, docentes y recomendaciones basadas en análisis de datos (scraping y feedback comunitario).

Actualmente, el sistema cuenta con un Backend robusto en Django REST Framework y un Frontend en React (Vite). Se han completado refactorizaciones mayores en la base de datos y la configuración del entorno.

## 2. Arquitectura del Sistema

### 2.1 Backend (Django)

* **Tecnología**: Django 6.0, Django REST Framework.
* **Estructura**: Modular, con aplicaciones separadas por dominio.
* **Configuración**: Sistema de settings modular (`base`, `development`, `production`, `test`) seleccionable vía variable de entorno.

#### Aplicaciones Principales

1. **Academic**:
    * Gestiona la oferta académica.
    * **Modelos Clave**:
        * `Comision` (antes Catedra): Representa una clase específica. Campos: código, horario, cuatrimestre.
        * `Docente`: Nuevo modelo para gestionar profesores independientemente de las comisiones.
2. **Recommendations**:
    * Núcleo del sistema de recomendaciones.
    * **Modelos Clave**:
        * `Recomendacion`: Vincula Comisiones con opiniones (Posts scrapeados).
        * **Nuevos Campos**: `prob_aprobar`, `asistencia`, `toma_tp`, `docent_perf` (análisis de perfil docente).
3. **Scraping**:
    * Motor de extracción de datos (Facebook/Redes).
    * Gestiona `Grupos`, `Tareas` (ahora con flag `activa`) y `Sesiones` de scraping.
4. **Users**:
    * Gestión de usuarios personalizada (basada en `AbstractUser`).

### 2.2 Frontend (React)

* **Tecnología**: React + Vite + TypeScript.
* **Estilos**: Tailwind CSS.
* **Puerto Desarrollo**: 3000.
* **Integración**: Construye (`npm run build`) hacia `backend/static/frontend` para ser servido por Django en producción/integración.
* **Componentes Clave**:
  * `Sidebar`: Navegación principal.
  * `ScrapingCenter`: Panel de control para tareas de scraping.
  * `Catedras` / `Recommendations`: Vistas principales de datos.

### 2.3 Base de Datos

* **Desarrollo/Test**: SQLite (`db.sqlite3` / `:memory:`).
* **Producción**: Configurado para PostgreSQL mediante `dj_database_url`.
* **Estado Actual**:
  * Migraciones actualizadas y aplicadas.
  * Refactorización `Catedra` -> `Comision` completada exitosamente.

## 3. Calidad y Testing

Se ha implementado una estrategia de **Testing Centralizado**:

* **Ubicación**: `backend/tests/`.
* **Cobertura**:
  * `test_models.py`: Pruebas unitarias de integridad de datos y relaciones.
  * `test_api.py`: Pruebas de integración de endpoints (API REST).
* **Estado**: 9 tests ejecutados y pasando (OK).
* **Diagramas**: Script de generación de diagramas Mermaid disponible en `backend/utils/diagram_generator.py`.

## 4. Cambios Recientes Importantes

1. **Refactorización de Modelos**:
    * Se eliminó el modelo monolítico `Catedra` y se reemplazó por `Comision` + `Docente` para normalizar la base de datos.
    * Se enriqueció el modelo `Recomendacion` con métricas específicas (probabilidad de aprobar, asistencia, etc.).
2. **Configuración Modular**:
    * Se migró de un `settings.py` único a una carpeta `config/settings/` con entornos diferenciados.
3. **Infraestructura de Pruebas**:
    * Limpieza de archivos temporales y centralización de scripts de prueba.

## 5. Próximos Pasos Sugeridos

1. **Completar Scraper**: Implementar la lógica real de extracción en `scraping` (actualmente estructura base).
2. **Dashboard Frontend**: Conectar los gráficos del Dashboard con los nuevos endpoints de métricas de recomendaciones.
3. **CI/CD**: Configurar pipeline de despliegue usando los nuevos settings de `production` y `test`.
