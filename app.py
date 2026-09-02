import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="PDF Chat", page_icon=":material/auto_awesome:", layout="wide")

ICON_PATHS = {
    "bot-message-square": '<path d="M12 6V2H8"/><path d="M15 11v2"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="M20 16a2 2 0 0 1-2 2H8.828a2 2 0 0 0-1.414.586l-2.202 2.202A.71.71 0 0 1 4 20.286V8a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2z"/><path d="M9 11v2"/>',
    "folder-open": '<path d="m6 14 1.45-2.9A2 2 0 0 1 9.24 10H20a2 2 0 0 1 1.94 2.5l-1.55 6a2 2 0 0 1-1.94 1.5H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h3.9a2 2 0 0 1 1.69.9l.81 1.2a2 2 0 0 0 1.67.9H18a2 2 0 0 1 2 2v2"/>',
    "upload-cloud": '<path d="M12 3v12"/><path d="m17 8-5-5-5 5"/><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>',
    "hourglass": '<path d="M5 22h14"/><path d="M5 2h14"/><path d="M17 22v-4.172a2 2 0 0 0-.586-1.414L12 12l-4.414 4.414A2 2 0 0 0 7 17.828V22"/><path d="M7 2v4.172a2 2 0 0 0 .586 1.414L12 12l4.414-4.414A2 2 0 0 0 17 6.172V2"/>',
    "check-circle": '<path d="M21.801 10A10 10 0 1 1 17 3.335"/><path d="m9 11 3 3L22 4"/>',
    "cpu": '<rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M15 2v2"/><path d="M15 20v2"/><path d="M2 15h2"/><path d="M2 9h2"/><path d="M20 15h2"/><path d="M20 9h2"/><path d="M9 2v2"/><path d="M9 20v2"/>',
}


def icon(name: str, size: int = 18, color: str = "var(--accent-cyan)") -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" '
        f'stroke-linecap="round" stroke-linejoin="round" '
        f'style="vertical-align:-{size * 0.15:.0f}px;display:inline-block">'
        f'{ICON_PATHS[name]}</svg>'
    )


def fish_svg(color: str) -> str:
    return (
        '<svg viewBox="0 0 100 50" xmlns="http://www.w3.org/2000/svg">'
        f'<path d="M20 25 L0 8 L0 42 Z" fill="{color}"/>'
        f'<ellipse cx="55" cy="25" rx="40" ry="18" fill="{color}"/>'
        '<circle cx="80" cy="19" r="3" fill="var(--bg)"/>'
        "</svg>"
    )

THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;500;600&display=swap');

:root {
    --bg: #0a0a0c;
    --accent-pink: #ff2e9f;
    --accent-amber: #ffb020;
    --accent-cyan: #00e5ff;
    --text-main: #f4f1fb;
    --text-muted: #a99fc9;
}

.stApp {
    background: var(--bg);
    font-family: 'Inter', sans-serif;
    color: var(--text-main);
}

h1, h1 span {
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    color: var(--text-main) !important;
}

h2, h3, h4 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--text-main) !important;
}

[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.03);
    backdrop-filter: blur(16px);
    border-right: 1px solid rgba(255,255,255,0.08);
}

[data-testid="stFileUploaderDropzone"] {
    background: rgba(255,255,255,0.04);
    border: 2px dashed rgba(255,176,32,0.5);
    border-radius: 18px;
}

[data-testid="stExpander"] {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
}

.stButton > button {
    border-radius: 999px !important;
    border: none !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em;
    background: rgba(255,255,255,0.06);
    color: var(--text-main) !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,229,255,0.25);
}
[data-testid="stBaseButton-primary"],
[data-testid="stBaseButton-primaryFormSubmit"] {
    background: rgba(255,255,255,0.10) !important;
    border: 1px solid rgba(255,255,255,0.22) !important;
    backdrop-filter: blur(10px);
    color: var(--text-main) !important;
    box-shadow: 0 4px 18px rgba(255,176,32,0.25);
}

[data-testid="stChatMessageContent"] p,
[data-testid="stChatMessageContent"] li,
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {
    color: var(--text-main) !important;
}

[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 4px 8px;
    margin-bottom: 12px;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    border-left: 3px solid var(--accent-cyan);
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    border-left: 3px solid var(--accent-pink);
}

[data-testid="stChatInput"] {
    border-radius: 999px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
}
[data-testid="stChatInput"] > div {
    background: transparent !important;
    border-color: transparent !important;
}
[data-testid="stChatInput"]:focus-within > div {
    border-color: var(--accent-cyan) !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: var(--accent-cyan) !important;
}
[data-testid="stChatInput"] textarea {
    color: var(--text-main) !important;
    caret-color: var(--text-main);
}
[data-testid="stChatInput"] textarea::placeholder {
    color: var(--text-muted) !important;
    opacity: 1;
}

[data-testid="stAlert"] {
    border-radius: 16px;
    background: rgba(255,255,255,0.05);
}

[data-testid="stTextInputRootElement"] {
    background: transparent !important;
    border-radius: 999px !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
}
[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.06) !important;
    color: var(--text-main) !important;
}
[data-testid="stTextInput"] input::placeholder {
    color: var(--text-muted) !important;
}

::-webkit-scrollbar { width: 10px; }
::-webkit-scrollbar-thumb {
    background: rgba(255,255,255,0.16);
    border-radius: 10px;
}

.gz-caption {
    color: var(--text-muted);
    font-size: 0.85rem;
}

[data-testid="stAppViewContainer"] {
    position: relative;
    z-index: 1;
}

.fish-tank {
    position: fixed;
    inset: 0;
    overflow: hidden;
    pointer-events: none;
    z-index: 0;
}
.bg-fish {
    position: absolute;
    left: -10vw;
    opacity: 0.18;
}
.bg-fish svg { width: 100%; height: 100%; display: block; }
.bg-fish-1 {
    top: 14%;
    width: clamp(56px, 7vw, 110px);
    animation: swimA 26s ease-in-out infinite;
}
.bg-fish-2 {
    top: 66%;
    width: clamp(42px, 5.5vw, 85px);
    animation: swimB 32s ease-in-out infinite;
    animation-delay: -9s;
}

/* swim right across the tank, flip, swim back */
@keyframes swimA {
    0%   { transform: translateX(0)     translateY(0)     scaleX(1); }
    45%  { transform: translateX(84vw)  translateY(-16px) scaleX(1); }
    50%  { transform: translateX(84vw)  translateY(-16px) scaleX(-1); }
    95%  { transform: translateX(0)     translateY(12px)  scaleX(-1); }
    100% { transform: translateX(0)     translateY(0)     scaleX(1); }
}
@keyframes swimB {
    0%   { transform: translateX(0)     translateY(0)    scaleX(1); }
    45%  { transform: translateX(68vw)  translateY(14px) scaleX(1); }
    50%  { transform: translateX(68vw)  translateY(14px) scaleX(-1); }
    95%  { transform: translateX(0)     translateY(-10px) scaleX(-1); }
    100% { transform: translateX(0)     translateY(0)    scaleX(1); }
}

@media (max-width: 640px) {
    .fish-tank { display: none; }
}
@media (prefers-reduced-motion: reduce) {
    .bg-fish { animation: none; }
}
</style>
"""
st.markdown(THEME_CSS, unsafe_allow_html=True)

st.markdown(
    '<div class="fish-tank">'
    f'<div class="bg-fish bg-fish-1">{fish_svg("var(--accent-cyan)")}</div>'
    f'<div class="bg-fish bg-fish-2">{fish_svg("var(--accent-pink)")}</div>'
    "</div>",
    unsafe_allow_html=True,
)

APP_PASSWORD = os.getenv("APP_PASSWORD")

if APP_PASSWORD:
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        _, mid, _ = st.columns([1, 1.2, 1])
        with mid:
            st.markdown(
                f'<h1>{icon("bot-message-square", 34, "var(--accent-pink)")} Chat with your PDFs</h1>',
                unsafe_allow_html=True,
            )
            st.markdown(
                '<p class="gz-caption">This app is password-protected.</p>',
                unsafe_allow_html=True,
            )
            with st.form("login_form"):
                pwd = st.text_input(
                    "Password",
                    type="password",
                    label_visibility="collapsed",
                    placeholder="Enter password",
                )
                submitted = st.form_submit_button(
                    "Enter", icon=":material/lock_open:", type="primary", use_container_width=True
                )
            if submitted:
                if pwd == APP_PASSWORD:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Incorrect password.", icon=":material/error:")
        st.stop()

try:
    from rag_engine import EmbeddingIndex, GROQ_MODEL, ask_groq, check_rate_limit, chunk_text, load_pdf
except RuntimeError as exc:
    st.error(str(exc), icon=":material/error:")
    st.stop()

if "index" not in st.session_state:
    st.session_state.index = EmbeddingIndex()
if "messages" not in st.session_state:
    st.session_state.messages = []
if "page_count" not in st.session_state:
    st.session_state.page_count = 0

with st.sidebar:
    st.markdown(
        f'<h2 style="display:flex;align-items:center;gap:8px;">'
        f'{icon("folder-open", 22, "var(--accent-amber)")} Documents</h2>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<p style="display:flex;align-items:center;gap:6px;font-weight:600;margin-bottom:4px;">'
        f'{icon("upload-cloud", 16)} Upload PDF(s)</p>',
        unsafe_allow_html=True,
    )
    uploaded_files = st.file_uploader(
        "Upload PDF(s)",
        type="pdf",
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    with st.expander("Settings", icon=":material/tune:"):
        chunk_size = st.slider("Chunk size", 500, 2000, 1000, step=100)
        overlap = st.slider("Chunk overlap", 0, 400, 150, step=50)
        top_k = st.slider("Chunks retrieved per question", 1, 10, 4)

    if st.button(
        "Process documents",
        icon=":material/bolt:",
        type="primary",
        disabled=not uploaded_files,
        use_container_width=True,
    ):
        with st.spinner("Reading and indexing documents...", show_time=True):
            all_chunks = []
            total_pages = 0
            for f in uploaded_files:
                text, page_count = load_pdf(f)
                total_pages += page_count
                all_chunks.extend(chunk_text(text, chunk_size, overlap))

            if all_chunks:
                st.session_state.index.build(all_chunks)
                st.session_state.messages = []
                st.session_state.page_count = total_pages
                st.success(
                    f"Indexed {len(all_chunks)} chunks from {len(uploaded_files)} file(s) "
                    f"— {total_pages} page(s) total.",
                    icon=":material/check_circle:",
                )
            else:
                st.warning("No extractable text found in the uploaded file(s).", icon=":material/warning:")

    if st.session_state.index.chunk_count:
        st.markdown(
            f'<p class="gz-caption">{icon("check-circle", 14, "var(--accent-cyan)")} Index ready — '
            f'{st.session_state.index.chunk_count} chunks · {st.session_state.page_count} page(s)</p>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<p class="gz-caption">{icon("hourglass", 14)} No documents indexed yet</p>',
            unsafe_allow_html=True,
        )

    st.divider()
    st.markdown(
        f'<p class="gz-caption">{icon("cpu", 14)} Model: <code>{GROQ_MODEL}</code></p>',
        unsafe_allow_html=True,
    )

    if st.button("Clear session", icon=":material/delete_sweep:", use_container_width=True):
        st.session_state.index = EmbeddingIndex()
        st.session_state.messages = []
        st.session_state.page_count = 0
        st.rerun()

st.markdown(
    f'<h1>{icon("bot-message-square", 34, "var(--accent-pink)")} Chat with your PDFs</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="gz-caption">Drop a doc, ask anything, get instant answers powered by '
    "<b>Groq</b> + <b>FAISS</b> retrieval.</p>",
    unsafe_allow_html=True,
)

if not st.session_state.index.chunk_count:
    st.info("Upload a PDF in the sidebar and click **Process documents** to get started.", icon=":material/upload_file:")

for message in st.session_state.messages:
    avatar = ":material/face:" if message["role"] == "user" else ":material/smart_toy:"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
        if message.get("sources"):
            with st.expander("Sources", icon=":material/description:"):
                for i, chunk in enumerate(message["sources"], 1):
                    st.markdown(f"**Chunk {i}**")
                    st.text(chunk)

question = st.chat_input(
    "Ask a question about your documents...",
    disabled=not st.session_state.index.chunk_count,
)

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user", avatar=":material/face:"):
        st.markdown(question)

    if not check_rate_limit():
        answer = "This app is getting a lot of questions right now — please wait a moment and try again."
        with st.chat_message("assistant", avatar=":material/smart_toy:"):
            st.warning(answer, icon=":material/hourglass_empty:")
        st.session_state.messages.append(
            {"role": "assistant", "content": answer, "sources": []}
        )
    else:
        sources = st.session_state.index.search(question, k=top_k)
        history = [
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages[:-1]
        ]

        with st.chat_message("assistant", avatar=":material/smart_toy:"):
            answer = st.write_stream(ask_groq(question, sources, history))
            if sources:
                with st.expander("Sources", icon=":material/description:"):
                    for i, chunk in enumerate(sources, 1):
                        st.markdown(f"**Chunk {i}**")
                        st.text(chunk)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer, "sources": sources}
        )
