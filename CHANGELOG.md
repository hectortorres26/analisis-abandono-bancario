# Cambios respecto a la versión original

## Revisión técnica y editorial — 2026-11-10

| Problema original | Corrección |
|---|---|
| Variables `df`/`data` inconsistentes, selección binaria como tupla y argumento `ncols` incompleto | Carga y validación centralizadas; cuaderno ejecutable de principio a fin |
| Columnas categóricas eliminadas antes de utilizarlas y correlaciones sobre objetos | Segmentación con categorías conservadas y correlaciones solo numéricas |
| Gráficas sin respuesta cuantificada sobre abandono | Tasas, denominadores e intervalos por segmento; tablas y gráficos regenerables |
| Dependencia de rutas de Colab/Drive | Entradas locales configurables, dependencias fijadas y pruebas |

Se añaden pruebas, dependencias fijadas, fuentes documentadas y resultados de ejecución. Las cifras nuevas corresponden al protocolo y los datasets identificados en esta revisión.

**Trazabilidad:** [cuaderno original](https://github.com/hectortorres26/analisis-abandono-bancario/blob/f527704abd53c9d7a21cb0a651236eb891b827c8/analisis_bancario.ipynb) · [comparación completa](https://github.com/hectortorres26/analisis-abandono-bancario/compare/f527704abd53c9d7a21cb0a651236eb891b827c8...main) · [historial](https://github.com/hectortorres26/analisis-abandono-bancario/commits/main).
