from django.views.generic import TemplateView
from django.db import models
from django.db.models import F
from academic.models import Comision
from recommendations.models import Recomendacion
from scraping.models import Grupos, Tarea_Scrapeo, Post_Scrapeado, Sesion_Scraping


class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Contar estadísticas
        context['stats'] = {
            'total_catedras': Comision.objects.count(),
            'total_posts': Post_Scrapeado.objects.count(),
            'total_recommendations': Recomendacion.objects.count(),
            'active_sessions': Sesion_Scraping.objects.filter(estado='en_progreso').count(),
        }
        
        # Top cátedras por recomendaciones
        context['top_catedras'] = Comision.objects.annotate(
            recommendation_count=models.Count('recomendaciones'),
            bar_height=models.ExpressionWrapper(
                models.Count('recomendaciones') * 20,
                output_field=models.IntegerField()
            ),
        ).order_by('-recommendation_count')[:5]
        
        # Sesiones recientes
        context['recent_sessions'] = Sesion_Scraping.objects.order_by('-inicio')[:5]
        context['today'] = __import__('datetime').date.today()
        
        return context


class CatedrasView(TemplateView):
    template_name = 'catedras.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catedras'] = Comision.objects.select_related('docente').annotate(
            recommendation_count=models.Count('recomendaciones')
        )
        return context


class RecommendationsView(TemplateView):
    template_name = 'recommendations.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recommendations'] = Recomendacion.objects.select_related(
            'comision', 'post_origen'
        ).annotate(
            conf_pct=models.ExpressionWrapper(F('confianza') * 100.0, output_field=models.FloatField())
        ).order_by('-id')
        return context


class ScrapingView(TemplateView):
    template_name = 'scraping.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grupos'] = Grupos.objects.all()
        context['tareas'] = Tarea_Scrapeo.objects.all()
        context['unprocessed_posts_count'] = Post_Scrapeado.objects.filter(
            recomendaciones__isnull=True
        ).count()
        return context


class HistoryView(TemplateView):
    template_name = 'history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sesiones'] = Sesion_Scraping.objects.order_by('-inicio')
        return context
