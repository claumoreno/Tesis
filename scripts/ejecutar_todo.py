# -*- coding: utf-8 -*-
"""Ejecuta todas las etapas en orden. Uso: python scripts/ejecutar_todo.py"""

import subprocess
import sys
from pathlib import Path

CARPETA = Path(__file__).resolve().parent
PASOS = ["00_validar_funciones.py", "01_limpieza_diagnostico.py", "02_red_indicadores.py",
         "03_validacion_panel.py", "04_entregables.py"]

for paso in PASOS:
    print(f"\n=== {paso} ===", flush=True)
    r = subprocess.run([sys.executable, str(CARPETA / paso)], cwd=CARPETA)
    if r.returncode != 0:
        sys.exit(f"Se detuvo en {paso}")
print("\nListo. Resultados en output/")
