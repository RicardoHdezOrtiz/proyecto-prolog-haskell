# Proyecto Final: Programación Lógica y Funcional

Sistema multiparadigma en línea de comandos que integra **Python**, **SWI-Prolog** y **Haskell (GHC)** mediante comunicación entre procesos (`subprocess`).

## Arquitectura del Proyecto

- `main.py`: Orquestador CLI, interfaz con colores y gestión de historial.
- `experto.pl`: Sistema Experto de diagnóstico de hardware en SWI-Prolog.
- `calculadora.hs`: Calculadora analítica funcional pura en Haskell.
- `.gitignore`: Exclusión de archivos temporales y salidas de sesión.
- `README.md`: Documentación del proyecto.

## Requisitos Previos

- **Python 3.10+**
- **SWI-Prolog (`swipl`)** agregado al `PATH`
- **Haskell GHC (`runghc`)** agregado al `PATH`

## Instalación y Ejecución

    git clone https://github.com/RicardoHdezOrtiz/proyecto-prolog-haskell.git
    cd proyecto-prolog-haskell
    python3 main.py

## Módulos Implementados

1. **Sistema Experto (`experto.pl`):** Motor de inferencia dinámico (`assertz/1` y `findall/3`) con 10 reglas de diagnóstico de PC, detección de múltiples fallas simultáneas y clasificación por nivel de urgencia (`CRITICA`, `ALTA`, `MEDIA`, `BAJA`).
2. **Calculadora Analítica (`calculadora.hs`):** Implementación funcional pura con recursividad (`factorial`, `mcd`), evaluación perezosa con listas infinitas (`fibonacci`), funciones de orden superior (`filter`, `foldl`, `mapM`) y validación segura con `Maybe`.
3. **Orquestador CLI (`main.py`):** Menú interactivo con selección numérica de síntomas, formato ANSI, verificación de entornos y exportación de historial de sesión a `.txt`.