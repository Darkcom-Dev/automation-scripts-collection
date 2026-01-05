<!-- .github/copilot-instructions.md
   Breve guía para agentes AI que colaboren en este repositorio.
   Mantener ~20-50 líneas, específicas y accionables. -->

# Contexto rápido

Este repositorio es una colección de utilidades Python pequeñas y autocontenidas (scripts CLI) enfocadas en tareas de automatización: creación de proyectos, manejo de licencias, procesamiento de PDFs, manipulación de texturas, convertidores OCR y utilidades de consola. Cada subcarpeta suele ser un script ejecutable independiente.

## Qué debe saber un agente antes de editar

- Scripts: cada carpeta contiene un script ejecutable (p. ej. `create-python-projects/create_python_project.py`, `licenser/licenser.py`, `pdf-manipulator/pdfmanipulator.py`). Mantener la filosofía: scripts simples, pocas dependencias externas.
- Convenciones de nombres: archivos de proyecto y documentación pueden usar kebab-case (p. ej. `base64-encriptor`) mientras que los scripts Python usan snake_case.
- Entorno: muchos scripts crean o asumen un virtualenv. Recomienda usar `python3 -m venv venv` y no introducir dependencias innecesarias.

## Comandos y flujos de desarrollo (detectables desde el repo)

- Hacer ejecutable un script: `chmod +x <script.py>` y ejecutar con `./script.py` o `python3 script.py`.
- Para crear proyectos de ejemplo, usar `create-python-projects/create_python_project.py` (interactivo). No asumas flags adicionales.
- Para añadir licencias, revisar `licenser/licenses/` y `licenser/licenser.py` para el formato esperado.

## Patrones de implementación observados

- Scripts orientados a la consola: pocas dependencias, uso directo de `argparse`/`input()` para CLI. Cuando agregues flags, usa `argparse` y conserva compatibilidad con entrada interactiva.
- Archivos `res/` contienen recursos y salidas de ejemplo (p. ej. `img-to-text/res/`). No modificar sin motivo.
- Evitar cambios masivos de formato: el repo contiene muchos scripts independientes; mantén cambios localizados y con pruebas manuales simples (ejecutar el script en modo `--help` o con un input mínimo).

## Qué revisar en un PR

- Asegurar que el script sigue ejecutable por `python3 script.py` y que la función principal está protegida por `if __name__ == '__main__'`.
- No añadir dependencias globales sin actualizary `requeriments.txt` o `requirements.txt` en la carpeta correspondiente.
- Documentar cualquier nuevo flag en el `README.md` raíz o en la subcarpeta `Readme.md` correspondiente.

## Ejemplos concretos (referencias)

- Para crear estructura de proyecto: `create-python-projects/create_python_project.py` — busca `venv/`, `src/`, `.gitignore` y plantilla `main.py`.
- Licencias: `licenser/licenses/` contiene plantillas de licencia; `licenser/licenser.py` muestra cómo se integran.
- OCR y recursos: `img-to-text/_img2txt.py` y `img-to-text/res/` muestran manejo de entradas y outputs en archivos.

Si algo no está claro o detectas un patrón adicional en el código, deja un comentario en el PR y propón una pequeña mejora explicando el motivo.
