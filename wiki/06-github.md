# GitHub

## Repositorio

[github.com/Tuldor/humanity-last-exam](https://github.com/Tuldor/humanity-last-exam) (privado)

## Rama principal

`main`

## Qué se versiona

| Incluido | Excluido |
|---|---|
| `src/app.py` | `.venv/` (entorno virtual) |
| `.streamlit/config.toml` | `data/` (dataset local) |
| `Iniciar.command` | `__pycache__/` |
| `wiki/` | `.DS_Store` |
| `.gitignore` | |

El dataset no se versiona porque es un fichero binario de ~270 MB que se descarga desde Hugging Face en la primera ejecución.

## Flujo de trabajo

```bash
# Clonar
git clone https://github.com/Tuldor/humanity-last-exam.git
cd humanity-last-exam

# Recrear entorno y descargar dataset (ver Instalación)
/opt/homebrew/bin/python3 -m venv .venv
.venv/bin/pip install streamlit datasets huggingface_hub pandas pillow

# Subir cambios
git add <ficheros>
git commit -m "descripción"
git push origin main
```

## Despliegue automático

Cada push a `main` activa un despliegue automático en Streamlit Cloud (~1-2 minutos).

Ver [Despliegue en Streamlit Cloud](08-streamlit-cloud.md) para:
- Primer despliegue
- Configuración de secretos
- Solución de problemas
- Monitoreo
