"""Recalcula con LibreOffice (headless) y revisa errores y Estado de Cargos contra Python."""
import sys, os, subprocess, json, shutil, openpyxl
XLSX, W = sys.argv[1], sys.argv[2]
prof = os.path.abspath(f'{W}/lo_profile'); out = os.path.abspath(f'{W}/lo_out')
os.makedirs(f'{prof}/user', exist_ok=True); os.makedirs(out, exist_ok=True)
open(f'{prof}/user/registrymodifications.xcu', 'w').write('''<?xml version="1.0" encoding="UTF-8"?>
<oor:items xmlns:oor="http://openoffice.org/2001/registry" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<item oor:path="/org.openoffice.Office.Calc/Formula/Load"><prop oor:name="OOXMLRecalcMode" oor:op="fuse"><value>0</value></prop></item>
<item oor:path="/org.openoffice.Office.Calc/Formula/Load"><prop oor:name="ODFRecalcMode" oor:op="fuse"><value>0</value></prop></item>
</oor:items>''')
subprocess.run(['soffice', f'-env:UserInstallation=file://{prof}', '--headless', '--calc', '--convert-to', 'xlsx',
                '--outdir', out, XLSX], check=True, capture_output=True, timeout=900)
wb = openpyxl.load_workbook(os.path.join(out, os.path.basename(XLSX)), data_only=True, read_only=True)
errs = []
for ws in wb.worksheets:
    if ws.title in ('board', 'Base_final', 'Directorios', 'Directores', 'Empresa_año'):
        continue
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, str) and c.value.startswith('#') and c.value.rstrip('!?').upper() in ('#REF', '#NAME', '#VALUE', '#DIV/0', '#N/A', '#NUM', '#NULL'):
                errs.append((ws.title, c.coordinate, c.value))
res = json.load(open(f'{W}/resumen_build.json'))
ws = wb['Cargos']
lo = [r[24] for r in ws.iter_rows(min_row=2, max_row=1 + len(res['estados_python']), values_only=True)]
ok = lo == res['estados_python']
rs = wb['Resumen']
tot = [c for c in next(rs.iter_rows(min_row=20, max_row=20, values_only=True))]
print('errores:', errs[:10], len(errs)); print('Estado LO == Python:', ok, lo[:5]); print('Resumen Total:', tot)
