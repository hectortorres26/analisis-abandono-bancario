# Análisis exploratorio del abandono bancario

Proyecto de **Hector Americo Torres Huamani** · Python y análisis de datos.

[Ver cuaderno](analisis_bancario.ipynb) · [Abrir original en Colab](https://colab.research.google.com/drive/1dDmVJvDxUcYsjv2zlkreuUqyE-fgIPHM) · [Portafolio](https://www.datascienceportfol.io/hectortorres26/projects/0)

## Objetivo y contenido

Estudiar las características de clientes de un banco y explorar su relación con el abandono (`churn`). El cuaderno describe un conjunto de 10 000 registros y 12 variables.

### Trabajo incluido

Lectura de datos, revisión de nulos, estadística descriptiva y visualizaciones de variables demográficas y financieras. Es un análisis exploratorio, no un modelo predictivo entrenado.

### Datos

Archivo esperado: `Bank Customer Churn Prediction.csv`.
Fuente indicada en el cuaderno: [Bank Customer Churn Dataset, Kaggle](https://www.kaggle.com/datasets/gauravtopre/bank-customer-churn-dataset).

### Revisión técnica

- La celda 13 (numeración desde 1) contiene `ncols=` sin valor: impide ejecutar esa celda.
- Se alternan `data` y `df` sin definir `df` en el cuaderno.
- La selección de columnas binarias usa una tupla y un tabulador antes de `credit_card`; debería seleccionar una lista de nombres válidos.
- Se eliminan `gender` y `country` antes de visualizaciones que las necesitan.
- La correlación necesita seleccionar explícitamente variables numéricas en versiones actuales de pandas. La matriz de correlación de correlaciones tampoco equivale a la correlación original de las variables.
- El original revisado contiene dos salidas con `KeyError`. El cuaderno aún no establece una conclusión reproducible sobre los grupos de mayor riesgo.

### Próximo paso recomendado

Corregir la ejecución secuencial, conservar las variables necesarias para las gráficas y comparar tasas de abandono por grupo junto con sus tamaños de muestra. Las asociaciones exploratorias no demuestran causalidad.

## Estado de esta publicación

Se conserva el código y el texto del cuaderno original. En la copia pública se retiraron las salidas guardadas, los contadores de ejecución y los metadatos de las celdas para no publicar identificadores ni datos financieros de clientes. El original se conserva localmente. La revisión del 9 de noviembre de 2026 fue estática: lectura del código, salidas y estructura. No se ejecutó el análisis con los datasets ni se corrigió silenciosamente el trabajo original. Los problemas anteriores deben resolverse antes de considerar reproducibles los resultados.

## Cómo explorar el proyecto

1. Abra el enlace de Colab o el archivo `.ipynb` en GitHub para consultar el trabajo.
2. Para trabajar localmente, cree un entorno virtual con `python -m venv .venv` y actívelo.
3. Instale las dependencias con `python -m pip install -r requirements.txt`.
4. Obtenga los datos desde su fuente autorizada. Ajuste las rutas `/content/drive/MyDrive/DATA_PRACTICA/` al directorio donde los haya guardado.
5. En un entorno local, omita las celdas de montaje de Google Drive, si las hay.
6. Resuelva los puntos de la revisión técnica y reinicie el kernel antes de ejecutar todas las celdas en orden.

`requirements.txt` enumera las librerías utilizadas; las versiones del entorno original no están registradas y no se ha validado una combinación exacta de versiones. Los datasets no se incluyen en este repositorio.

## Autoría y procedencia

Publicado a partir del cuaderno enlazado en el portafolio del autor. Las fuentes y licencias de los datos son independientes de la autoría del análisis. Esta publicación no añade una licencia de redistribución al código ni a los datasets.
