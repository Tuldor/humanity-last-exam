# Instalación y configuración

## Requisitos

- macOS
- Python 3.14
- Cuenta en [Hugging Face](https://huggingface.co) con acceso aceptado al dataset `cais/hle`

## Entorno virtual

El proyecto usa un entorno virtual Python en `.venv/`. Para recrearlo desde cero:

```bash
cd "/Users/noriol/Google Drive - Mi Unidad/noriol/Abedul 3/NOH/VS Code Projects/Humanity Last Exam"
/opt/homebrew/bin/python3 -m venv .venv
.venv/bin/pip install streamlit datasets huggingface_hub pandas pillow
```

## Configuración de Streamlit

Fichero `.streamlit/config.toml`:

```toml
[browser]
gatherUsageStats = false

[server]
headless = true
address = "localhost"
port = 8503
```

| Parámetro | Valor | Motivo |
|---|---|---|
| `gatherUsageStats` | false | No enviar telemetría a Streamlit |
| `headless` | true | Evitar el onboarding interactivo al arrancar |
| `address` | localhost | Restringir acceso solo al equipo local |
| `port` | 8503 | Puerto fijo para no colisionar con otros proyectos |

## Primera ejecución — descarga del dataset

El dataset `cais/hle` es *gated* (requiere aceptar términos en Hugging Face). La descarga es única: los datos se guardan en `data/hle.parquet` y en ejecuciones posteriores se usan directamente sin conexión.

Pasos:

1. Ve a [huggingface.co/datasets/cais/hle](https://huggingface.co/datasets/cais/hle) y acepta los términos (aprobación automática).
2. Genera un token *read* en [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).
3. Abre la app, pega el token en el campo que aparece y pulsa **Descargar dataset**.
4. La descarga tarda unos minutos (~270 MB). Una vez completada, la app carga directamente sin pedir el token.

## Arranque

### Opción A — Doble clic (recomendada)
Abre el Finder, navega a la carpeta del proyecto y haz doble clic en `Iniciar.command`. Se abre una terminal, arranca el servidor y el navegador se abre automáticamente en `http://localhost:8503`.

### Opción B — Terminal
```bash
cd "/Users/noriol/Google Drive - Mi Unidad/noriol/Abedul 3/NOH/VS Code Projects/Humanity Last Exam"
.venv/bin/streamlit run src/app.py
```

## Seguridad

La aplicación solo acepta conexiones desde `localhost`, por lo que no es accesible desde otros dispositivos de la red ni desde internet.
