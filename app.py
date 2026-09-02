import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="PDF Chat", page_icon=":material/auto_awesome:", layout="wide")

st.markdown(
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link rel="stylesheet" '
    'href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;500;600&display=swap">',
    unsafe_allow_html=True,
)

ICON_PATHS = {
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


THEME_CSS = """
<style>
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

[data-testid="stBottom"] > div {
    background: transparent !important;
}

[data-testid="stChatInput"] {
    border-radius: 999px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
}
[data-testid="stChatInput"] > div {
    background: transparent !important;
    border: none !important;
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

[data-testid="stHeader"] {
    background: transparent !important;
}

/* Streamlit hides the sidebar collapse arrow until hover by default - keep it visible. */
[data-testid="stSidebarCollapseButton"] {
    visibility: visible !important;
    opacity: 0.85 !important;
    transition: opacity 0.15s ease;
}
[data-testid="stSidebarCollapseButton"]:hover {
    opacity: 1 !important;
}

.stApp {
    animation: appFadeIn 0.5s ease;
}
@keyframes appFadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
@media (prefers-reduced-motion: reduce) {
    .stApp { animation: none; }
}

.shards-bg {
    position: fixed;
    inset: 0;
    overflow: hidden;
    pointer-events: none;
    z-index: 0;
    background:
        radial-gradient(ellipse 60% 50% at 80% 12%, rgba(255,46,159,0.10), transparent 60%),
        radial-gradient(ellipse 55% 45% at 12% 88%, rgba(0,229,255,0.09), transparent 60%),
        var(--bg);
}
.shard {
    position: absolute;
    mix-blend-mode: screen;
    filter: blur(2.5px);
    will-change: transform, opacity;
    animation-name: shardDrift;
    animation-timing-function: ease-in-out;
    animation-iteration-count: infinite;
}
.shard-a { clip-path: polygon(0% 45%, 22% 0%, 100% 32%, 78% 100%, 0% 68%); }
.shard-b { clip-path: polygon(12% 0%, 100% 22%, 88% 100%, 0% 78%); }
.shard-c { clip-path: polygon(0% 22%, 100% 0%, 82% 62%, 28% 100%); }

@keyframes shardDrift {
    0%, 100% {
        transform: translate(0, 0) rotate(var(--rot0, -4deg));
        opacity: var(--op-lo, 0.28);
    }
    50% {
        transform: translate(var(--dx, 3vw), var(--dy, 2vh)) rotate(var(--rot1, 5deg));
        opacity: var(--op-hi, 0.5);
    }
}

@media (prefers-reduced-motion: reduce) {
    .shard { animation: none; opacity: var(--op-hi, 0.4); }
}
</style>
"""
st.markdown(THEME_CSS, unsafe_allow_html=True)

_SHARDS = [
    dict(shape="a", top="4%", left="68%", w="150px", h="60px", rot="-18deg",
         grad="135deg, rgba(0,229,255,0.30), rgba(0,229,255,0.02)",
         dx="2.5vw", dy="-1.5vh", rot0="-18deg", rot1="-12deg", op_lo="0.14", op_hi="0.26",
         dur="24s", delay="0s"),
    dict(shape="b", top="14%", left="84%", w="110px", h="46px", rot="12deg",
         grad="120deg, rgba(255,46,159,0.28), rgba(255,46,159,0.02)",
         dx="-2vw", dy="2vh", rot0="12deg", rot1="20deg", op_lo="0.12", op_hi="0.22",
         dur="30s", delay="1.5s"),
    dict(shape="c", top="2%", left="46%", w="90px", h="90px", rot="4deg",
         grad="150deg, rgba(255,176,32,0.24), rgba(255,176,32,0.02)",
         dx="1.5vw", dy="2.5vh", rot0="4deg", rot1="-3deg", op_lo="0.08", op_hi="0.16",
         dur="28s", delay="3s"),
    dict(shape="b", top="60%", left="90%", w="130px", h="54px", rot="-30deg",
         grad="140deg, rgba(0,229,255,0.26), rgba(0,229,255,0.02)",
         dx="-2.5vw", dy="-2vh", rot0="-30deg", rot1="-22deg", op_lo="0.10", op_hi="0.20",
         dur="34s", delay="0.8s"),
    dict(shape="a", top="78%", left="8%", w="140px", h="58px", rot="10deg",
         grad="130deg, rgba(255,46,159,0.26), rgba(255,46,159,0.02)",
         dx="2vw", dy="-2vh", rot0="10deg", rot1="4deg", op_lo="0.10", op_hi="0.20",
         dur="26s", delay="2s"),
    dict(shape="c", top="42%", left="-4%", w="100px", h="100px", rot="-8deg",
         grad="145deg, rgba(255,176,32,0.20), rgba(255,176,32,0.02)",
         dx="1.8vw", dy="1.5vh", rot0="-8deg", rot1="-2deg", op_lo="0.07", op_hi="0.14",
         dur="32s", delay="4s"),
    dict(shape="b", top="6%", left="16%", w="80px", h="34px", rot="20deg",
         grad="120deg, rgba(0,229,255,0.22), rgba(0,229,255,0.02)",
         dx="-1.5vw", dy="1.8vh", rot0="20deg", rot1="28deg", op_lo="0.07", op_hi="0.14",
         dur="22s", delay="2.6s"),
    dict(shape="a", top="88%", left="54%", w="120px", h="48px", rot="-14deg",
         grad="135deg, rgba(255,255,255,0.16), rgba(255,255,255,0.01)",
         dx="2vw", dy="-1.5vh", rot0="-14deg", rot1="-8deg", op_lo="0.05", op_hi="0.10",
         dur="29s", delay="1s"),
]

_shard_divs = "".join(
    f'<div class="shard shard-{s["shape"]}" style="'
    f'top:{s["top"]};left:{s["left"]};width:{s["w"]};height:{s["h"]};'
    f'background:linear-gradient({s["grad"]});'
    f'--rot0:{s["rot0"]};--rot1:{s["rot1"]};--dx:{s["dx"]};--dy:{s["dy"]};'
    f'--op-lo:{s["op_lo"]};--op-hi:{s["op_hi"]};'
    f'animation-duration:{s["dur"]};animation-delay:{s["delay"]};'
    f'transform:rotate({s["rot"]});"></div>'
    for s in _SHARDS
)
st.markdown(f'<div class="shards-bg">{_shard_divs}</div>', unsafe_allow_html=True)

APP_PASSWORD = os.getenv("APP_PASSWORD")

if APP_PASSWORD:
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        _, mid, _ = st.columns([1, 1.2, 1])
        with mid:
            st.markdown(
                "<h1>Chat with your PDFs</h1>",
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
    "<h1>Chat with your PDFs</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="gz-caption">Drop a doc, ask anything, get instant answers powered by '
    "<b>Groq</b> + <b>FAISS</b> retrieval.</p>",
    unsafe_allow_html=True,
)

if not st.session_state.index.chunk_count:
    st.info(
        "Upload a PDF in the sidebar and click **Process documents** to get started. "
        "On a phone, tap the **»** icon in the top-left corner first to open the sidebar.",
        icon=":material/upload_file:",
    )
    st.markdown(
        """
        <style>
        [data-testid="stExpandSidebarButton"] {
            animation: hintPulse 2s ease-in-out infinite;
            border-radius: 999px;
        }
        @keyframes hintPulse {
            0%, 100% { box-shadow: 0 0 0 0 rgba(0,229,255,0.5); }
            50% { box-shadow: 0 0 0 6px rgba(0,229,255,0); }
        }
        @media (prefers-reduced-motion: reduce) {
            [data-testid="stExpandSidebarButton"] { animation: none; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

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
