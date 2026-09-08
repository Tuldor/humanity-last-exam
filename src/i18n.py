"""Internationalization (i18n) module for Humanity's Last Exam."""

TRANSLATIONS = {
    "en": {
        # Page & title
        "page_title": "Humanity's Last Exam — Browser",

        # Sidebar filters
        "filters_header": "Filters",
        "category": "Category",
        "category_placeholder": "All categories",
        "theme": "Theme (raw_subject)",
        "theme_placeholder": "All themes",
        "answer_type": "Answer Type",
        "answer_type_placeholder": "All types",
        "has_image": "Has image?",
        "has_image_all": "All",
        "has_image_with": "With image",
        "has_image_without": "Without image",
        "search_questions": "Search in question",
        "search_placeholder": "keywords…",
        "language": "Language / Idioma",
        "total_dataset": "Total in dataset",
        "questions_unit": "questions",

        # Results
        "questions_match": "questions match the filters.",
        "no_results": "No questions match the selected filters.",

        # Pagination
        "page": "Page",
        "page_of": "Page",

        # Question cards
        "category_label": "Category",
        "theme_label": "Theme",
        "answer_type_label": "Answer Type",
        "author_label": "Author",
        "id_label": "ID",
        "question_label": "Question",
        "associated_image": "Associated image",
        "show_answer": "Show answer",
        "answer_label": "Answer",
        "rationale_label": "Rationale",
        "image_unavailable": "(image not available)",
    },
    "es": {
        # Page & title
        "page_title": "🧠 Humanity's Last Exam — Navegador",

        # Sidebar filters
        "filters_header": "Filtros",
        "category": "Categoría",
        "category_placeholder": "Todas las categorías",
        "theme": "Tema (raw_subject)",
        "theme_placeholder": "Todos los temas",
        "answer_type": "Tipo de respuesta",
        "answer_type_placeholder": "Todos los tipos",
        "has_image": "¿Tiene imagen?",
        "has_image_all": "Todas",
        "has_image_with": "Con imagen",
        "has_image_without": "Sin imagen",
        "search_questions": "Buscar en el enunciado",
        "search_placeholder": "palabras clave…",
        "language": "Language / Idioma",
        "total_dataset": "Total en dataset",
        "questions_unit": "preguntas",

        # Results
        "questions_match": "preguntas coinciden con los filtros.",
        "no_results": "No hay preguntas que coincidan con los filtros seleccionados.",

        # Pagination
        "page": "Página",
        "page_of": "de",

        # Question cards
        "category_label": "Categoría",
        "theme_label": "Tema",
        "answer_type_label": "Tipo respuesta",
        "author_label": "Autor",
        "id_label": "ID",
        "question_label": "Pregunta",
        "associated_image": "Imagen asociada",
        "show_answer": "Mostrar respuesta",
        "answer_label": "Respuesta",
        "rationale_label": "Razonamiento / Rationale",
        "image_unavailable": "(imagen no disponible)",
    }
}


def get_text(key: str, language: str = "en") -> str:
    """Get translated text for a key in the specified language.

    Args:
        key: Translation key
        language: Language code ('en' or 'es')

    Returns:
        Translated string or the key if translation not found
    """
    return TRANSLATIONS.get(language, TRANSLATIONS["en"]).get(key, key)
