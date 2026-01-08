#!/usr/bin/env python
"""
Script de debugging para identificar puntos calientes en Academic app.

Uso:
    python debug_academic.py [opción]

Opciones:
    queries     - Detecta problemas N+1
    duplicates  - Busca datos duplicados
    orphans     - Encuentra comisiones sin docente
    stats       - Estadísticas generales
    all         - Ejecuta todas las comprobaciones
"""

import os
import sys
import django

# Setup Django - ensure we're in the right directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection, reset_queries
from django.test.utils import override_settings
from django.db.models import Count, Q
from academic.models import Docente, Comision


class Colors:
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'


def print_header(title):
    print(f"\n{Colors.BLUE}{'='*60}{Colors.NC}")
    print(f"{Colors.BLUE}{title:^60}{Colors.NC}")
    print(f"{Colors.BLUE}{'='*60}{Colors.NC}\n")


def check_n_plus_one_queries():
    """Detecta problemas N+1 en queries."""
    print_header("🔍 Detección de Queries N+1")
    
    with override_settings(DEBUG=True):
        reset_queries()
        
        # Test 1: Listar docentes (debería ser 1 query)
        print("📋 Test 1: Listar todos los docentes")
        docentes = list(Docente.objects.all())
        queries_count = len(connection.queries)
        
        if queries_count <= 1:
            print(f"{Colors.GREEN}✅ OK: {queries_count} query{Colors.NC}")
        else:
            print(f"{Colors.RED}❌ PROBLEMA: {queries_count} queries (esperado: 1){Colors.NC}")
            for i, q in enumerate(connection.queries, 1):
                print(f"   Query {i}: {q['sql'][:100]}...")
        
        # Test 2: Acceder a comisiones de cada docente (debería usar prefetch)
        reset_queries()
        print("\n📋 Test 2: Acceder a comisiones de todos los docentes")
        docentes = Docente.objects.prefetch_related('comisiones')
        for d in docentes:
            _ = list(d.comisiones.all())
        
        queries_count = len(connection.queries)
        if queries_count <= 2:
            print(f"{Colors.GREEN}✅ OK: {queries_count} queries (con prefetch_related){Colors.NC}")
        else:
            print(f"{Colors.RED}❌ PROBLEMA N+1: {queries_count} queries{Colors.NC}")
            print(f"{Colors.YELLOW}   Sin prefetch_related habrían sido {len(docentes) + 1} queries{Colors.NC}")
        
        # Test 3: Listar comisiones con docente (debería usar select_related)
        reset_queries()
        print("\n📋 Test 3: Listar comisiones y acceder a su docente")
        comisiones = Comision.objects.select_related('docente')
        for c in comisiones[:10]:  # Solo primeras 10
            if c.docente:
                _ = c.docente.nombre
        
        queries_count = len(connection.queries)
        if queries_count == 1:
            print(f"{Colors.GREEN}✅ OK: {queries_count} query (con select_related){Colors.NC}")
        else:
            print(f"{Colors.RED}❌ PROBLEMA: {queries_count} queries{Colors.NC}")


def check_duplicates():
    """Busca docentes y comisiones duplicadas."""
    print_header("🔄 Detección de Duplicados")
    
    # Docentes duplicados por nombre completo
    print("👤 Docentes con nombre completo duplicado:")
    duplicados = Docente.objects.values(
        'nombre_completo'
    ).annotate(
        count=Count('id_docente')
    ).filter(count__gt=1).order_by('-count')
    
    if duplicados:
        for d in duplicados:
            docentes = Docente.objects.filter(nombre_completo=d['nombre_completo'])
            print(f"{Colors.YELLOW}⚠️  '{d['nombre_completo']}' - {d['count']} registros:{Colors.NC}")
            for doc in docentes:
                print(f"    ID: {doc.id_docente}, Comisiones: {doc.comisiones.count()}")
    else:
        print(f"{Colors.GREEN}✅ No hay docentes duplicados{Colors.NC}")
    
    # Docentes duplicados por apellido+nombre (case insensitive)
    print("\n👤 Posibles duplicados (case-insensitive):")
    docentes = Docente.objects.all()
    nombres_vistos = {}
    
    for d in docentes:
        key = f"{d.nombre} {d.apellido}".lower()
        if key in nombres_vistos:
            print(f"{Colors.YELLOW}⚠️  Posible duplicado:{Colors.NC}")
            print(f"    1) ID {nombres_vistos[key].id_docente}: {nombres_vistos[key].nombre_completo}")
            print(f"    2) ID {d.id_docente}: {d.nombre_completo}")
        else:
            nombres_vistos[key] = d
    
    if len(nombres_vistos) == len(docentes):
        print(f"{Colors.GREEN}✅ No hay duplicados case-insensitive{Colors.NC}")
    
    # Comisiones duplicadas por código
    print("\n📚 Comisiones con código duplicado:")
    dup_comisiones = Comision.objects.values(
        'codigo'
    ).annotate(
        count=Count('id_comision')
    ).filter(count__gt=1)
    
    if dup_comisiones:
        for c in dup_comisiones:
            print(f"{Colors.RED}❌ Código '{c['codigo']}' duplicado {c['count']} veces{Colors.NC}")
    else:
        print(f"{Colors.GREEN}✅ No hay comisiones duplicadas{Colors.NC}")


def check_orphans():
    """Encuentra registros huérfanos o inconsistentes."""
    print_header("🏚️  Detección de Registros Huérfanos")
    
    # Comisiones sin docente
    sin_docente = Comision.objects.filter(docente__isnull=True)
    count_sin_docente = sin_docente.count()
    
    print(f"📚 Comisiones sin docente asignado: {count_sin_docente}")
    if count_sin_docente > 0:
        print(f"{Colors.YELLOW}⚠️  Primeras 5:{Colors.NC}")
        for c in sin_docente[:5]:
            print(f"    - {c.codigo}: {c.nombre}")
    else:
        print(f"{Colors.GREEN}✅ Todas las comisiones tienen docente{Colors.NC}")
    
    # Docentes sin comisiones
    print("\n👤 Docentes sin comisiones asignadas:")
    sin_comisiones = Docente.objects.annotate(
        num_comisiones=Count('comisiones')
    ).filter(num_comisiones=0)
    
    count_sin_comisiones = sin_comisiones.count()
    print(f"   Total: {count_sin_comisiones}")
    
    if count_sin_comisiones > 0:
        print(f"{Colors.YELLOW}⚠️  Primeros 10:{Colors.NC}")
        for d in sin_comisiones[:10]:
            print(f"    - {d.nombre_completo}")
    else:
        print(f"{Colors.GREEN}✅ Todos los docentes tienen al menos 1 comisión{Colors.NC}")
    
    # Comisiones con códigos sospechosos
    print("\n📚 Comisiones con códigos sospechosos:")
    sospechosos = Comision.objects.filter(
        Q(codigo__icontains='None') |
        Q(codigo__icontains='null') |
        Q(codigo__exact='') |
        Q(codigo__regex=r'^\s+$')
    )
    
    if sospechosos.exists():
        print(f"{Colors.RED}❌ Encontrados {sospechosos.count()} códigos sospechosos:{Colors.NC}")
        for c in sospechosos[:5]:
            print(f"    - '{c.codigo}': {c.nombre}")
    else:
        print(f"{Colors.GREEN}✅ No hay códigos sospechosos{Colors.NC}")


def show_stats():
    """Muestra estadísticas generales."""
    print_header("📊 Estadísticas Generales")
    
    total_docentes = Docente.objects.count()
    total_comisiones = Comision.objects.count()
    
    print(f"👤 Total docentes: {total_docentes}")
    print(f"📚 Total comisiones: {total_comisiones}")
    
    if total_docentes > 0:
        promedio = total_comisiones / total_docentes
        print(f"📈 Promedio comisiones por docente: {promedio:.2f}")
    
    # Docentes con más comisiones
    print("\n🏆 Top 5 docentes con más comisiones:")
    top_docentes = Docente.objects.annotate(
        num_comisiones=Count('comisiones')
    ).order_by('-num_comisiones')[:5]
    
    for i, d in enumerate(top_docentes, 1):
        print(f"   {i}. {d.nombre_completo}: {d.num_comisiones} comisiones")
    
    # Distribución de comisiones
    print("\n📊 Distribución de comisiones por docente:")
    distribucion = Docente.objects.annotate(
        num_comisiones=Count('comisiones')
    ).values('num_comisiones').annotate(
        count=Count('id_docente')
    ).order_by('num_comisiones')
    
    for d in distribucion[:10]:
        num = d['num_comisiones']
        count = d['count']
        bar = '█' * min(count, 50)
        print(f"   {num:2d} comisiones: {bar} ({count} docentes)")
    
    # Comisiones por cuatrimestre
    print("\n📅 Comisiones por cuatrimestre:")
    por_cuatrimestre = Comision.objects.exclude(
        cuatrimestre__isnull=True
    ).values('cuatrimestre').annotate(
        count=Count('id_comision')
    ).order_by('-cuatrimestre')
    
    for c in por_cuatrimestre[:5]:
        print(f"   {c['cuatrimestre']}: {c['count']} comisiones")


def main():
    option = sys.argv[1] if len(sys.argv) > 1 else 'all'
    
    print(f"{Colors.GREEN}🔧 Academic App Debugger{Colors.NC}")
    
    if option in ['queries', 'all']:
        check_n_plus_one_queries()
    
    if option in ['duplicates', 'all']:
        check_duplicates()
    
    if option in ['orphans', 'all']:
        check_orphans()
    
    if option in ['stats', 'all']:
        show_stats()
    
    if option == 'help':
        print(__doc__)
    
    print(f"\n{Colors.GREEN}✅ Análisis completado{Colors.NC}\n")


if __name__ == '__main__':
    main()
