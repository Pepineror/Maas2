#!/usr/bin/env python3
"""
Script de ejemplo para ejecutar el test suite completo
y mostrar un resumen de los resultados.

Uso:
    python3 run_tests.py                    # Ejecutar todas las pruebas
    python3 run_tests.py TestListProjects   # Ejecutar una clase específica
    python3 run_tests.py -v                 # Modo verbose
"""

import sys
import subprocess
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Ejecutor de pruebas para RedmineExtractor"
    )
    parser.add_argument(
        "test_class",
        nargs="?",
        default="",
        help="Clase de pruebas específica a ejecutar (ej: TestListProjects)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Modo verbose"
    )
    parser.add_argument(
        "--coverage",
        action="store_true",
        help="Generar reporte de cobertura"
    )
    parser.add_argument(
        "--html",
        action="store_true",
        help="Generar reporte HTML"
    )
    
    args = parser.parse_args()
    
    # Construir comando pytest
    cmd = ["python3", "-m", "pytest"]
    
    test_file = "backend/tests/test_redmine_extractor_complete.py"
    if args.test_class:
        test_file += f"::{args.test_class}"
    
    cmd.append(test_file)
    
    if args.verbose:
        cmd.append("-v")
    else:
        cmd.append("-v")  # Por defecto siempre verbose
    
    if args.coverage:
        cmd.extend(["--cov=backend.tools", "--cov-report=term-missing"])
    
    if args.html:
        cmd.extend(["--html=test_report.html", "--self-contained-html"])
    
    # Añadir opciones adicionales
    cmd.append("--tb=short")
    cmd.append("-ra")  # Mostrar resumen de todos los resultados
    
    print("🧪 Ejecutando test suite completo para RedmineExtractor")
    print(f"📝 Comando: {' '.join(cmd)}")
    print("=" * 80)
    
    # Ejecutar
    result = subprocess.run(cmd)
    
    print("=" * 80)
    if result.returncode == 0:
        print("✅ ¡TODAS LAS PRUEBAS PASARON!")
    else:
        print("❌ Algunas pruebas fallaron")
    
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
