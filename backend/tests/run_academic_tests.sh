#!/bin/bash
# Script para ejecutar tests de Academic con opciones útiles

set -e

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🧪 Academic App Test Runner${NC}"
echo ""

# Función para ejecutar tests
run_test() {
    echo -e "${YELLOW}➜ $1${NC}"
    python manage.py test $2 --verbosity=2
    echo ""
}

# Menú
case "${1:-all}" in
    models)
        echo "📦 Testing Models..."
        run_test "Docente Model" "academic.tests.DocenteModelTest"
        run_test "Comision Model" "academic.tests.ComisionModelTest"
        ;;
    
    serializers)
        echo "🔄 Testing Serializers..."
        run_test "Docente Serializers" "academic.tests.DocenteSerializerTest"
        run_test "Comision Serializers" "academic.tests.ComisionSerializerTest"
        ;;
    
    api)
        echo "🌐 Testing API..."
        run_test "Docente API" "academic.tests.DocenteAPITest"
        run_test "Comision API" "academic.tests.ComisionAPITest"
        ;;
    
    search)
        echo "🔍 Testing Search..."
        run_test "Search functionality" "tests.test_academic_search"
        ;;
    
    import)
        echo "📥 Testing Import..."
        run_test "CSV Import" "academic.tests.ImportComisionesCommandTest"
        ;;
    
    performance)
        echo "⚡ Testing Performance..."
        run_test "Query Optimization" "academic.tests.QueryOptimizationTest"
        ;;
    
    edge)
        echo "🔬 Testing Edge Cases..."
        run_test "Edge Cases" "academic.tests.EdgeCasesTest"
        ;;
    
    coverage)
        echo "📊 Running with Coverage..."
        coverage run --source='academic' manage.py test academic.tests
        coverage report
        coverage html
        echo -e "${GREEN}✅ Coverage report generated in htmlcov/index.html${NC}"
        ;;
    
    watch)
        echo "👀 Watching for changes..."
        while true; do
            python manage.py test academic.tests --verbosity=1
            echo -e "\n${YELLOW}Waiting for changes... (Ctrl+C to stop)${NC}"
            sleep 5
        done
        ;;
    
    quick)
        echo "⚡ Quick test (most important)..."
        python manage.py test academic.tests.DocenteModelTest academic.tests.DocenteAPITest --verbosity=1
        ;;
    
    all)
        echo "🚀 Running ALL Academic tests..."
        python manage.py test academic.tests --verbosity=2
        echo -e "${GREEN}✅ All tests completed!${NC}"
        ;;
    
    help|--help|-h)
        echo "Usage: ./run_academic_tests.sh [option]"
        echo ""
        echo "Options:"
        echo "  models      - Test Docente and Comision models"
        echo "  serializers - Test serializers"
        echo "  api         - Test API endpoints"
        echo "  search      - Test search functionality"
        echo "  import      - Test CSV/Excel import"
        echo "  performance - Test query optimization"
        echo "  edge        - Test edge cases"
        echo "  coverage    - Run with coverage report"
        echo "  watch       - Watch mode (re-run on changes)"
        echo "  quick       - Quick test (most important)"
        echo "  all         - Run all tests (default)"
        echo "  help        - Show this help"
        echo ""
        echo "Examples:"
        echo "  ./run_academic_tests.sh models"
        echo "  ./run_academic_tests.sh api"
        echo "  ./run_academic_tests.sh coverage"
        ;;
    
    *)
        echo -e "${RED}❌ Unknown option: $1${NC}"
        echo "Use './run_academic_tests.sh help' for usage"
        exit 1
        ;;
esac

echo -e "${GREEN}✅ Done!${NC}"
