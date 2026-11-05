# Simulación de máquinas y líneas de producción con Flask

Aplicación web que carga máquinas y productos desde XML, calcula pasos de producción, simula el proceso y presenta diagramas/reporte de tiempos.

## Requisitos

Python 3, dependencias de requerimientos.txt y Graphviz dot en PATH. El nombre del manifiesto es requerimientos.txt.

## Ejecución

Los comandos parten de la raíz del repositorio, salvo donde se indica otra terminal.

```bash
python -m pip install -r requerimientos.txt
python app.py
```

## Recorrido de demostración

Abrir http://127.0.0.1:5000, inicializar el estado, cargar uno de los XML de ejemplo y seleccionar máquina/producto. Comparar la simulación completa con la consulta por segundos. procesos.py contiene la lógica de la simulación.

## Organización

Carpetas de la entrega: [`documentacion/`](documentacion/), [`static/`](static/), [`templates/`](templates/).

## Alcance y límites

El estado es local al proceso y se reemplaza al inicializar/cargar. La simulación es académica; no hay análisis de telemetría en tiempo real.

## Contexto y licencia

Trabajo académico o de aprendizaje conservado en el portafolio de [Enner Mendizabal](https://github.com/Ennero). Los créditos de los trabajos en grupo se conservan en sus entregas y manuales.

Consultar [LICENSE](LICENSE) para la licencia de la raíz. Las dependencias y los componentes con avisos o licencias propios conservan sus condiciones.
