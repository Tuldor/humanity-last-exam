import streamlit as st
import pandas as pd
import os
import base64
from pathlib import Path
from io import BytesIO
from i18n import get_text

DATA_PATH = Path(__file__).parent.parent / "data" / "hle.parquet"
HF_DATASET = "cais/hle"


# ── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Humanity's Last Exam",
    page_icon="🧠",
    layout="wide",
)

# ── Initialize language in session state ────────────────────────────────────
if "language" not in st.session_state:
    st.session_state.language = "en"


# ── Authentication ──────────────────────────────────────────────────────────
def check_password():
    """Returns True if the user entered the correct password."""
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False

    if not st.session_state.password_correct:
        st.markdown("# 🔐 Acceso restringido")
        st.info("Por favor, ingresa la contraseña para acceder a la aplicación.")

        password = st.text_input("Contraseña", type="password", key="password_input")

        # Get the correct password from secrets or environment variable
        try:
            correct_password = st.secrets.get("app_password", None)
        except Exception:
            correct_password = None

        if not correct_password:
            correct_password = os.getenv("APP_PASSWORD", "")

        if not correct_password:
            st.error("⚠️ No hay contraseña configurada. Contacta al administrador.")
            return False

        if password:
            if password == correct_password:
                st.session_state.password_correct = True
                st.rerun()
            else:
                st.error("❌ Contraseña incorrecta. Intenta de nuevo.")
                return False

    return st.session_state.password_correct


# Check authentication before loading the rest of the app
if not check_password():
    st.stop()


lang = st.session_state.language
st.title(get_text("page_title", lang))


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
    st.header(get_text("filters_header", lang))

    # 1. Categoría
    all_categories = sorted(df["category"].dropna().unique().tolist())
    selected_categories = st.multiselect(
        get_text("category", lang),
        options=all_categories,
        default=[],
        placeholder=get_text("category_placeholder", lang),
    )

    # 2. Tema (raw_subject) — dependiente de la categoría
    if selected_categories:
        subject_pool = df[df["category"].isin(selected_categories)]["raw_subject"].dropna().unique()
    else:
        subject_pool = df["raw_subject"].dropna().unique()
    all_subjects = sorted(subject_pool.tolist())

    selected_subjects = st.multiselect(
        get_text("theme", lang),
        options=all_subjects,
        default=[],
        placeholder=get_text("theme_placeholder", lang),
    )

    # 3. Tipo de respuesta
    all_answer_types = sorted(df["answer_type"].dropna().unique().tolist())
    selected_answer_types = st.multiselect(
        get_text("answer_type", lang),
        options=all_answer_types,
        default=[],
        placeholder=get_text("answer_type_placeholder", lang),
    )

    # 4. Tiene imagen
    has_image_filter = st.radio(
        get_text("has_image", lang),
        options=[
            get_text("has_image_all", lang),
            get_text("has_image_with", lang),
            get_text("has_image_without", lang),
        ],
        index=0,
    )

    # 5. Búsqueda libre en el enunciado
    search_text = st.text_input(
        get_text("search_questions", lang),
        placeholder=get_text("search_placeholder", lang),
    )

    # 6. Language selector
    st.divider()
    language_options = {"English": "en", "Español": "es"}
    selected_lang_display = st.selectbox(
        get_text("language", lang),
        options=list(language_options.keys()),
        index=0 if st.session_state.language == "en" else 1,
        key="language_selector",
    )
    st.session_state.language = language_options[selected_lang_display]

    if st.session_state.language != lang:
        st.rerun()

    st.divider()
    st.caption(f"{get_text('total_dataset', lang)}: {len(df):,} {get_text('questions_unit', lang)}")


# ── Apply filters ────────────────────────────────────────────────────────────
filtered = df.copy()

if selected_categories:
    filtered = filtered[filtered["category"].isin(selected_categories)]

if selected_subjects:
    filtered = filtered[filtered["raw_subject"].isin(selected_subjects)]

if selected_answer_types:
    filtered = filtered[filtered["answer_type"].isin(selected_answer_types)]

has_image_with = get_text("has_image_with", lang)
has_image_without = get_text("has_image_without", lang)

if has_image_filter == has_image_with:
    filtered = filtered[filtered["image"].notna() & (filtered["image"] != "")]
elif has_image_filter == has_image_without:
    filtered = filtered[filtered["image"].isna() | (filtered["image"] == "")]

if search_text.strip():
    mask = filtered["question"].str.contains(search_text.strip(), case=False, na=False)
    filtered = filtered[mask]

# ── Results header ───────────────────────────────────────────────────────────
st.markdown(f"**{len(filtered):,}** {get_text('questions_match', lang)}")

if filtered.empty:
    st.warning(get_text("no_results", lang))
    st.stop()


# ── Pagination ───────────────────────────────────────────────────────────────
PAGE_SIZE = 10
total_pages = max(1, (len(filtered) - 1) // PAGE_SIZE + 1)

col_left, col_mid, col_right = st.columns([2, 1, 2])
with col_mid:
    page = st.number_input(get_text("page", lang), min_value=1, max_value=total_pages, value=1, step=1)

page_df = filtered.iloc[(page - 1) * PAGE_SIZE : page * PAGE_SIZE].reset_index(drop=True)

st.caption(f"{get_text('page', lang)} {page} {get_text('page_of', lang)} {total_pages}")
st.divider()


# ── Question cards ───────────────────────────────────────────────────────────
def render_image(image_val, lang):
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
            st.caption(f"_({get_text('image_unavailable', lang)})_")


for idx, row in page_df.iterrows():
    q_num = (page - 1) * PAGE_SIZE + idx + 1

    with st.expander(
        f"**#{q_num}** — {row.get('category', '—')} · {row.get('raw_subject', '—')}",
        expanded=False,
    ):
        # Metadata row
        meta_cols = st.columns(3)
        meta_cols[0].markdown(f"**{get_text('category_label', lang)}:** {row.get('category', '—')}")
        meta_cols[1].markdown(f"**{get_text('theme_label', lang)}:** {row.get('raw_subject', '—')}")
        meta_cols[2].markdown(f"**{get_text('answer_type_label', lang)}:** {row.get('answer_type', '—')}")

        st.markdown(f"**{get_text('author_label', lang)}:** {row.get('author_name', '—')}")
        st.markdown(f"**{get_text('id_label', lang)}:** `{row.get('id', '—')}`")

        st.divider()

        # Question
        st.markdown(f"**{get_text('question_label', lang)}:**")
        st.markdown(row.get("question", ""))

        # Image (if any)
        img = row.get("image", "")
        if img and not pd.isna(img):
            st.markdown(f"**{get_text('associated_image', lang)}:**")
            render_image(img, lang)

        st.divider()

        # Answer (revealed on demand)
        answer_col, _ = st.columns([1, 2])
        with answer_col:
            show_answer = st.checkbox(get_text("show_answer", lang), key=f"ans_{row.get('id', idx)}_{page}")

        if show_answer:
            if img and not pd.isna(img):
                render_image(img, lang)
            st.markdown(f"**{get_text('answer_label', lang)}:** {row.get('answer', '—')}")
            rationale = row.get("rationale", "")
            if rationale and not pd.isna(rationale) and str(rationale).strip():
                with st.expander(get_text("rationale_label", lang)):
                    st.markdown(str(rationale))
