# Estructura de ficheros

```
Humanity Last Exam/
├── src/
│   └── app.py              # Aplicación Streamlit
├── data/
│   └── hle.parquet         # Dataset local (no versionado)
├── wiki/                   # Esta documentación
│   ├── index.md
│   ├── 01-descripcion.md
│   ├── 02-estructura.md
│   ├── 03-instalacion.md
│   ├── 04-uso.md
│   ├── 05-arquitectura.md
│   └── 06-github.md
├── .streamlit/
│   └── config.toml         # Configuración de Streamlit
├── .venv/                  # Entorno virtual Python (no versionado)
├── .gitignore
└── Iniciar.command         # Script de arranque (doble clic en Finder)
```

## Ficheros principales

### src/app.py
Aplicación Streamlit completa. Contiene:
- Flujo de descarga del dataset (primera ejecución)
- Carga y caché del parquet local
- Lógica de filtros (categoría, tema, tipo de respuesta, imagen, búsqueda libre)
- Paginación
- Renderizado de tarjetas de pregunta con imagen y respuesta

### data/hle.parquet
Dataset descargado de Hugging Face y persistido localmente. No se versiona en git. Contiene las 2.500 preguntas con todos sus campos excepto las columnas de imagen binaria (`image_preview`, `rationale_image`), que se descartan para reducir peso. Las imágenes se conservan en la columna `image` como cadenas base64.

### Iniciar.command
Script bash para arrancar la app desde el Finder sin necesidad de abrir VSCode ni una terminal.

### .streamlit/config.toml
Configuración permanente de Streamlit (ver [Instalación y configuración](03-instalacion.md)).
