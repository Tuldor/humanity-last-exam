# Cómo usar la aplicación

## Pantalla principal

Al abrir la app se muestra el número total de preguntas que coinciden con los filtros activos, seguido de las tarjetas de pregunta paginadas (10 por página).

## Filtros

Todos los filtros están en la barra lateral izquierda y se aplican en tiempo real.

### Categoría
Selector múltiple con las 8 categorías del dataset. Si no se selecciona ninguna, se muestran todas.

### Tema (raw_subject)
Selector múltiple con los temas específicos. **Depende de la categoría**: si hay categorías seleccionadas, solo muestra los temas que pertenecen a esas categorías.

### Tipo de respuesta
Selector múltiple:
- `exactMatch` — respuesta abierta de texto exacto (1.909 preguntas)
- `multipleChoice` — opción múltiple (591 preguntas)

### ¿Tiene imagen?
Tres opciones: Todas / Con imagen / Sin imagen. Todas las preguntas del dataset tienen imagen, por lo que este filtro es útil principalmente para comprobación.

### Búsqueda libre
Filtra preguntas cuyo enunciado contenga las palabras clave indicadas (no distingue mayúsculas).

## Tarjetas de pregunta

Cada pregunta se muestra como un bloque desplegable con el formato:

```
#N — Categoría · Tema
```

Al expandirlo se muestra:
- Metadatos: categoría, tema, tipo de respuesta, autor e ID
- Enunciado completo
- Imagen asociada
- Checkbox **Mostrar respuesta**: al activarlo aparece la imagen de nuevo, la respuesta correcta y, si existe, el razonamiento del autor en un sub-desplegable

## Paginación

El selector de página se encuentra entre el encabezado de resultados y las tarjetas. Cada página muestra 10 preguntas.
