# Descripción del proyecto

Aplicación web local desarrollada con **Streamlit** para explorar las preguntas del benchmark **Humanity's Last Exam (HLE)**.

## Para qué sirve

HLE es un benchmark de inteligencia artificial creado por el Center for AI Safety (CAIS) formado por 2.500 preguntas de nivel experto en múltiples disciplinas. La aplicación permite navegar, filtrar y leer las preguntas y sus respuestas de forma cómoda sin necesidad de acceder a Hugging Face.

## Caso de uso

Revisión y estudio del benchmark: seleccionar preguntas por categoría o tema, leer sus enunciados e imágenes asociadas y consultar las respuestas y razonamientos.

## Fuente de datos

Dataset [`cais/hle`](https://huggingface.co/datasets/cais/hle) alojado en Hugging Face. Se descarga una sola vez con un token de usuario y se guarda localmente en `data/hle.parquet`.

## Características del dataset

| Campo | Descripción |
|---|---|
| `id` | Identificador único de la pregunta |
| `question` | Enunciado de la pregunta |
| `image` | Imagen asociada en base64 |
| `answer` | Respuesta correcta |
| `answer_type` | `exactMatch` o `multipleChoice` |
| `author_name` | Autor de la pregunta |
| `rationale` | Explicación de la respuesta |
| `raw_subject` | Tema específico (p.ej. *Mathematics*, *Chess*…) |
| `category` | Categoría agrupada (8 categorías) |

## Distribución por categoría

| Categoría | Preguntas |
|---|---|
| Math | 1.021 |
| Biology/Medicine | 280 |
| Computer Science/AI | 241 |
| Other | 233 |
| Physics | 230 |
| Humanities/Social Science | 219 |
| Chemistry | 165 |
| Engineering | 111 |
