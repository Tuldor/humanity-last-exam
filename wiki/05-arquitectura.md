# Arquitectura técnica

## Stack

| Capa | Tecnología |
|---|---|
| Interfaz | Streamlit 1.56 |
| Datos | Pandas + PyArrow (parquet) |
| Descarga | Hugging Face `datasets` + `huggingface_hub` |
| Imágenes | Pillow + base64 |
| Python | 3.14 (Homebrew) |

## Flujo de datos

```
Primera ejecución
    HuggingFace Hub (cais/hle)
        └── datasets.load_dataset()
            └── DataFrame.to_parquet()
                └── data/hle.parquet

Ejecuciones posteriores
    data/hle.parquet
        └── pd.read_parquet()  ← cacheado con @st.cache_data
            └── Filtros en memoria
                └── Streamlit UI
```

## Decisiones de diseño

### Parquet local
El dataset se guarda en parquet para evitar depender de conexión a internet tras la primera descarga y para carga rápida (<1 s gracias al caché de Streamlit).

### Columnas de imagen eliminadas en descarga
`image_preview` y `rationale_image` son columnas de tipo PIL Image binarias que duplican peso sin aportar nada extra: la columna `image` ya contiene la misma imagen como base64, lista para renderizar en el navegador.

### Imágenes en base64
Las imágenes vienen como `data:image/jpeg;base64,…` en el dataset original. La función `render_image()` intenta decodificarlas con `base64.b64decode` y, si falla, las trata como URL.

### Caché con @st.cache_data
La carga del parquet se cachea para que los filtros respondan en tiempo real sin releer el fichero en cada interacción.

### Filtro de tema dependiente
El selector de `raw_subject` se recalcula dinámicamente según las categorías seleccionadas, evitando mostrar temas que no tienen preguntas en el contexto actual.
