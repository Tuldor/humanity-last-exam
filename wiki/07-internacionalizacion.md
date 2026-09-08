# Internacionalización (i18n)

## Visión general

La aplicación soporta dos idiomas: **Inglés** (por defecto) y **Español**. El usuario puede cambiar el idioma desde un selector en el panel lateral sin perder los filtros ni la navegación.

## Características

- ✅ **Selector de idioma** en el sidebar como último filtro ("Language / Idioma")
- ✅ **Inglés por defecto** en la primera visita
- ✅ **Persistencia en sesión**: La preferencia de idioma se mantiene durante la sesión
- ✅ **Traducción completa**: Todos los elementos de UI están traducidos
- ✅ **Preguntas siempre en inglés**: El contenido del dataset se muestra en inglés independientemente del idioma seleccionado

## Estructura

### `src/i18n.py`
Módulo con todas las traducciones. Define:

```python
TRANSLATIONS = {
    "en": { ... },  # Inglés
    "es": { ... }   # Español
}

def get_text(key: str, language: str = "en") -> str:
    """Obtiene la traducción de una clave"""
```

**Claves traducidas:**
- `page_title`: Título de la página
- `filters_header`: Encabezado de filtros
- `category`, `theme`, `answer_type`, `has_image`, `search_questions`: Etiquetas de filtros
- `has_image_all`, `has_image_with`, `has_image_without`: Opciones del filtro de imagen
- `language`: Etiqueta del selector de idioma
- `questions_match`, `no_results`: Mensajes de resultados
- `page`, `page_of`: Paginación
- `category_label`, `theme_label`, `author_label`, `id_label`: Etiquetas en tarjetas
- `question_label`, `answer_label`, `rationale_label`: Secciones de pregunta
- `associated_image`: Etiqueta de imagen
- `show_answer`: Botón para mostrar respuesta
- `total_dataset`, `questions_unit`: Footer de total

### Flujo en `src/app.py`

```python
# 1. Inicializar idioma (por defecto "en")
if "language" not in st.session_state:
    st.session_state.language = "en"

# 2. Usar idioma actual en variables
lang = st.session_state.language

# 3. Obtener textos traducidos
st.markdown(get_text("page_title", lang))

# 4. Selector de idioma en sidebar
selected_lang_display = st.selectbox(
    get_text("language", lang),
    options=["English", "Español"],
    ...
)
st.session_state.language = language_options[selected_lang_display]

# Si cambió el idioma, re-renderizar
if st.session_state.language != lang:
    st.rerun()
```

## Agregar un nuevo idioma

Para agregar un nuevo idioma (p.ej. portugués):

1. **Actualizar `src/i18n.py`:**
   ```python
   TRANSLATIONS = {
       "en": { ... },
       "es": { ... },
       "pt": { "page_title": "...", ... }  # Agregar aquí
   }
   ```

2. **Actualizar selector en `src/app.py`:**
   ```python
   language_options = {
       "English": "en",
       "Español": "es",
       "Português": "pt"  # Agregar aquí
   }
   ```

3. **Traducir todas las claves** en el nuevo idioma

## Nota: Pantallas no traducidas

Las siguientes pantallas **mantienen el español original** por decisión de diseño:

- **Pantalla de autenticación** (contraseña)
- **Flujo de descarga del dataset** (instrucciones para Hugging Face)

Esto se debe a que son flujos de administración/configuración únicos, no parte de la experiencia principal del usuario.
