"""
Script de análisis y reporte de pruebas

Genera un análisis detallado del test suite incluyendo:
- Conteo de pruebas por categoría
- Cobertura de funcionalidad
- Estadísticas de ejecución
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple


class TestAnalyzer:
    def __init__(self, test_file: str):
        self.test_file = Path(test_file)
        self.content = self.test_file.read_text()
        self.test_classes = {}
        self.fixtures = []
        self.parse()
    
    def parse(self):
        """Parsea el archivo de pruebas para extraer información."""
        # Encontrar clases de prueba
        class_pattern = r'class (Test\w+).*?(?=class Test|\Z)'
        classes = re.findall(class_pattern, self.content, re.DOTALL)
        
        for class_name in classes:
            # Encontrar métodos de prueba en cada clase
            class_section = re.search(
                rf'class {class_name}.*?(?=class Test|\Z)',
                self.content,
                re.DOTALL
            )
            if class_section:
                methods = re.findall(
                    r'def (test_\w+)\(',
                    class_section.group(0)
                )
                self.test_classes[class_name] = methods
        
        # Encontrar fixtures
        fixture_pattern = r'@pytest\.fixture\s+def (\w+)\('
        self.fixtures = re.findall(fixture_pattern, self.content)
    
    def get_statistics(self) -> Dict:
        """Retorna estadísticas del test suite."""
        total_tests = sum(len(tests) for tests in self.test_classes.values())
        
        return {
            "total_test_classes": len(self.test_classes),
            "total_test_methods": total_tests,
            "total_fixtures": len(self.fixtures),
            "classes": self.test_classes,
            "fixtures": self.fixtures
        }
    
    def print_report(self):
        """Imprime un reporte formateado."""
        stats = self.get_statistics()
        
        print("\n" + "=" * 80)
        print("📊 ANÁLISIS DEL TEST SUITE - RedmineExtractor")
        print("=" * 80)
        
        # Resumen general
        print("\n📈 ESTADÍSTICAS GENERALES:")
        print(f"   ├─ Clases de Prueba:  {stats['total_test_classes']}")
        print(f"   ├─ Métodos de Prueba: {stats['total_test_methods']}")
        print(f"   └─ Fixtures:          {stats['total_fixtures']}")
        
        # Detalle por clase
        print("\n🧪 DESGLOSE POR CLASE:")
        for i, (class_name, methods) in enumerate(stats['classes'].items(), 1):
            category = self._get_category_emoji(class_name)
            print(f"   {i}. {category} {class_name}")
            print(f"      └─ {len(methods)} pruebas")
            for method in methods[:2]:  # Mostrar primeras 2
                print(f"         • {method}")
            if len(methods) > 2:
                print(f"         • ... y {len(methods) - 2} más")
        
        # Fixtures
        print("\n🔧 FIXTURES DISPONIBLES:")
        for i, fixture in enumerate(stats['fixtures'], 1):
            print(f"   {i}. {fixture}")
        
        # Cobertura de funcionalidad
        print("\n✨ COBERTURA DE FUNCIONALIDAD:")
        coverage_map = {
            'Init': 'Inicialización del extractor',
            'ListProjects': 'Listado de proyectos',
            'ListIssues': 'Listado de problemas',
            'GetIssueDetails': 'Detalles de problemas',
            'ListUsers': 'Listado de usuarios',
            'ListTrackers': 'Rastreadores',
            'ListStatuses': 'Estados de problemas',
            'ErrorHandling': 'Manejo de errores',
            'DataValidation': 'Validación de datos',
            'IntegrationScenarios': 'Escenarios de integración'
        }
        
        for key, description in coverage_map.items():
            for class_name in stats['classes'].keys():
                if key in class_name:
                    count = len(stats['classes'][class_name])
                    print(f"   ✓ {description}: {count} pruebas")
                    break
        
        # Resumen final
        print("\n" + "=" * 80)
        print(f"✅ TOTAL: {stats['total_test_methods']} pruebas listas para ejecutar")
        print("=" * 80 + "\n")
    
    @staticmethod
    def _get_category_emoji(class_name: str) -> str:
        """Retorna un emoji basado en el tipo de clase."""
        emojis = {
            'Init': '⚙️',
            'ListProjects': '📋',
            'ListIssues': '🎫',
            'GetIssueDetails': '🔍',
            'ListUsers': '👥',
            'ListTrackers': '🏷️',
            'ListStatuses': '📊',
            'ErrorHandling': '⚠️',
            'DataValidation': '✔️',
            'IntegrationScenarios': '🔗'
        }
        
        for key, emoji in emojis.items():
            if key in class_name:
                return emoji
        return '📝'


if __name__ == "__main__":
    test_file = Path(__file__).parent / "test_redmine_extractor_complete.py"
    
    if test_file.exists():
        analyzer = TestAnalyzer(str(test_file))
        analyzer.print_report()
    else:
        print(f"❌ Archivo no encontrado: {test_file}")
