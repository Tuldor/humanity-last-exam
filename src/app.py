import streamlit as st
import pandas as pd
import os
import base64
from pathlib import Path
from io import BytesIO

DATA_PATH = Path(__file__).parent.parent / "data" / "hle.parquet"
HF_DATASET = "cais/hle"


# ── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Humanity's Last Exam",
    page_icon="🧠",
    layout="wide",
)

st.title("🧠 Humanity's Last Exam — Browser")


# ── Dataset download / load ──────────────────────────────────────────────────

def download_dataset(token: str) -> str | None:
    """Download HLE from HuggingFace and save as parquet. Returns error string or None."""
    try:
        from datasets import load_dataset
        import huggingface_hub
        huggingface_hub.login(token=token, add_to_git_credential=False)
        with st.spinner("Descargando dataset (~270 MB)… esto puede tardar unos minutos."):
            ds = load_dataset(HF_DATASET, split="test", token=token)
            df = ds.to_pandas()
            # Drop heavy image columns (keep text only, images shown on demand)
            for col in ["image_preview", "rationale_image"]:
                if col in df.columns:
                    df = df.drop(columns=[col])
            DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
            df.to_parquet(DATA_PATH, index=False)
        return None
    except Exception as e:
        return str(e)


@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    return pd.read_parquet(DATA_PATH)


# ── Auth / first-run flow ────────────────────────────────────────────────────
if not DATA_PATH.exists():
    st.info(
        "El dataset **Humanity's Last Exam** está alojado en Hugging Face y requiere "
        "aceptar sus términos de uso. Solo necesitas hacerlo una vez: los datos se "
        "guardan localmente para usos posteriores."
    )
    st.markdown(
        "1. Ve a [cais/hle en Hugging Face](https://huggingface.co/datasets/cais/hle) "
        "y acepta los términos (acceso automático).\n"
        "2. Genera un token en [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) "
        "(permiso *read* es suficiente).\n"
        "3. Pégalo abajo y pulsa **Descargar**."
    )
    token = st.text_input("Token de Hugging Face", type="password", key="hf_token")
    if st.button("Descargar dataset", type="primary", disabled=not token):
        err = download_dataset(token)
        if err:
            st.error(f"Error al descargar: {err}")
        else:
            st.success("Dataset descargado correctamente.")
            st.rerun()
    st.stop()


# ── Load data ────────────────────────────────────────────────────────────────
df = load_data()


# ── Sidebar filters ──────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Filtros")

    # 1. Categoría
    all_categories = sorted(df["category"].dropna().unique().tolist())
    selected_categories = st.multiselect(
        "Categoría",
        options=all_categories,
        default=[],
        placeholder="Todas las categorías",
    )

    # 2. Tema (raw_subject) — dependiente de la categoría
    if selected_categories:
        subject_pool = df[df["category"].isin(selected_categories)]["raw_subject"].dropna().unique()
    else:
        subject_pool = df["raw_subject"].dropna().unique()
    all_subjects = sorted(subject_pool.tolist())

    selected_subjects = st.multiselect(
        "Tema (raw_subject)",
        options=all_subjects,
        default=[],
        placeholder="Todos los temas",
    )

    # 3. Tipo de respuesta
    all_answer_types = sorted(df["answer_type"].dropna().unique().tolist())
    selected_answer_types = st.multiselect(
        "Tipo de respuesta",
        options=all_answer_types,
        default=[],
        placeholder="Todos los tipos",
    )

    # 4. Tiene imagen
    has_image_filter = st.radio(
        "¿Tiene imagen?",
        options=["Todas", "Con imagen", "Sin imagen"],
        index=0,
    )

    # 5. Búsqueda libre en el enunciado
    search_text = st.text_input("Buscar en el enunciado", placeholder="palabras clave…")

    st.divider()
    st.caption(f"Total en dataset: {len(df):,} preguntas")


# ── Apply filters ────────────────────────────────────────────────────────────
filtered = df.copy()

if selected_categories:
    filtered = filtered[filtered["category"].isin(selected_categories)]

if selected_subjects:
    filtered = filtered[filtered["raw_subject"].isin(selected_subjects)]

if selected_answer_types:
    filtered = filtered[filtered["answer_type"].isin(selected_answer_types)]

if has_image_filter == "Con imagen":
    filtered = filtered[filtered["image"].notna() & (filtered["image"] != "")]
elif has_image_filter == "Sin imagen":
    filtered = filtered[filtered["image"].isna() | (filtered["image"] == "")]

if search_text.strip():
    mask = filtered["question"].str.contains(search_text.strip(), case=False, na=False)
    filtered = filtered[mask]

# ── Results header ───────────────────────────────────────────────────────────
st.markdown(f"**{len(filtered):,} preguntas** coinciden con los filtros.")

if filtered.empty:
    st.warning("No hay preguntas que coincidan con los filtros seleccionados.")
    st.stop()


# ── Pagination ───────────────────────────────────────────────────────────────
PAGE_SIZE = 10
total_pages = max(1, (len(filtered) - 1) // PAGE_SIZE + 1)

col_left, col_mid, col_right = st.columns([2, 1, 2])
with col_mid:
    page = st.number_input("Página", min_value=1, max_value=total_pages, value=1, step=1)

page_df = filtered.iloc[(page - 1) * PAGE_SIZE : page * PAGE_SIZE].reset_index(drop=True)

st.caption(f"Página {page} de {total_pages}")
st.divider()


# ── Question cards ───────────────────────────────────────────────────────────
def render_image(image_val):
    """Render image from base64 string or URL."""
    if not image_val or pd.isna(image_val):
        return
    try:
        # Try base64
        img_bytes = base64.b64decode(image_val)
        st.image(img_bytes, use_container_width=True)
    except Exception:
        # Try as URL
        try:
            st.image(image_val, use_container_width=True)
        except Exception:
            st.caption("_(imagen no disponible)_")


for idx, row in page_df.iterrows():
    q_num = (page - 1) * PAGE_SIZE + idx + 1

    with st.expander(
        f"**#{q_num}** — {row.get('category', '—')} · {row.get('raw_subject', '—')}",
        expanded=False,
    ):
        # Metadata row
        meta_cols = st.columns(3)
        meta_cols[0].markdown(f"**Categoría:** {row.get('category', '—')}")
        meta_cols[1].markdown(f"**Tema:** {row.get('raw_subject', '—')}")
        meta_cols[2].markdown(f"**Tipo respuesta:** {row.get('answer_type', '—')}")

        st.markdown(f"**Autor:** {row.get('author_name', '—')}")
        st.markdown(f"**ID:** `{row.get('id', '—')}`")

        st.divider()

        # Question
        st.markdown("**Pregunta:**")
        st.markdown(row.get("question", ""))

        # Image (if any)
        img = row.get("image", "")
        if img and not pd.isna(img):
            st.markdown("**Imagen asociada:**")
            render_image(img)

        st.divider()

        # Answer (revealed on demand)
        answer_col, _ = st.columns([1, 2])
        with answer_col:
            show_answer = st.checkbox("Mostrar respuesta", key=f"ans_{row.get('id', idx)}_{page}")

        if show_answer:
            if img and not pd.isna(img):
                render_image(img)
            st.markdown(f"**Respuesta:** {row.get('answer', '—')}")
            rationale = row.get("rationale", "")
            if rationale and not pd.isna(rationale) and str(rationale).strip():
                with st.expander("Razonamiento / Rationale"):
                    st.markdown(str(rationale))
