# Conexiones políticas: Seremis (prompt v3)

- `interlocking_db_seremis.xlsx`: entregable (formato de la plantilla de ministros + Directores, Directorios, Base_final, Empresa_año, board).
- `trabajo/resultados_parciales.csv`: avance de la búsqueda, una fila por director (estado, consulta, fecha, cargos en JSON).
- `insumos/`: base original, plantilla de ministros y prompt.
- `scripts/`: preparación (`prep.py`), lotes (`siguiente.py`, `registrar.py`), generación (`build_excel.py`) y control con LibreOffice (`check_lo.py`).

Para retomar (desde esta carpeta, con W=trabajo):

```bash
python3 scripts/prep.py insumos/interlocking_db.xlsx trabajo
python3 scripts/siguiente.py trabajo 25
python3 scripts/build_excel.py insumos/Base_Ministros_Chile_1980-2026.xlsx insumos/interlocking_db.xlsx trabajo interlocking_db_seremis.xlsx
python3 scripts/check_lo.py interlocking_db_seremis.xlsx trabajo
```
