import streamlit as st
import time
from dotenv import load_dotenv
from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarizer import summarize, generate_title
from core.extractor import extract_action_items, extract_key_decisions, extract_questions
from core.rag_engine import build_rag_chain, ask_question

load_dotenv()

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VideoVerse-AI",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@300;400;500&display=swap');

/* ── Root Variables ── */
:root {
    --bg: #06060a;
    --bg-2: #0b0b14;
    --surface: rgba(255,255,255,0.035);
    --surface-solid: #101018;
    --border: rgba(255,255,255,0.09);
    --border-hover: rgba(167,139,250,0.45);

    --violet: #8b5cf6;
    --violet-2: #a78bfa;
    --fuchsia: #e879f9;
    --cyan: #22d3ee;
    --amber: #fbbf24;

    --text: #f1f0f8;
    --text-dim: #9391b0;
    --text-faint: #5f5d78;

    --success: #34d399;
    --warning: #fbbf24;
    --danger: #fb7185;

    --radius: 16px;
    --radius-sm: 10px;
}

/* ── Global Reset ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

.stApp {
    background:
        radial-gradient(ellipse 900px 500px at 15% -10%, rgba(139,92,246,0.20), transparent 60%),
        radial-gradient(ellipse 700px 500px at 100% 0%, rgba(34,211,238,0.12), transparent 55%),
        radial-gradient(ellipse 800px 600px at 50% 120%, rgba(232,121,249,0.08), transparent 60%),
        var(--bg) !important;
}

/* subtle floating orbs, purely decorative */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        radial-gradient(1px 1px at 20% 30%, rgba(255,255,255,0.25) 0%, transparent 100%),
        radial-gradient(1px 1px at 70% 65%, rgba(255,255,255,0.18) 0%, transparent 100%),
        radial-gradient(1.5px 1.5px at 85% 20%, rgba(255,255,255,0.2) 0%, transparent 100%),
        radial-gradient(1px 1px at 40% 80%, rgba(255,255,255,0.15) 0%, transparent 100%);
    background-size: 100% 100%;
    pointer-events: none;
    z-index: 0;
}

section.main > div { position: relative; z-index: 1; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(16,16,24,0.98), rgba(10,10,17,0.98)) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] * {
    color: var(--text) !important;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
}

/* ── Headings ── */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--text) !important;
}

/* ── Brand Lockup (sidebar) ── */
.brand-mark {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 0.3rem;
}
.brand-icon {
    width: 38px; height: 38px;
    border-radius: 11px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.15rem;
    background: linear-gradient(135deg, var(--violet), var(--fuchsia));
    box-shadow: 0 4px 20px rgba(139,92,246,0.45);
    flex-shrink: 0;
}
.brand-name {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.25rem;
    font-weight: 800;
    letter-spacing: -0.01em;
    line-height: 1.1;
    background: linear-gradient(135deg, #ffffff 0%, var(--violet-2) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.brand-tag {
    font-size: 0.68rem;
    color: var(--text-faint);
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-left: 48px;
    margin-top: -4px;
}

/* ── Hero Title (main) ── */
.hero-wrap { padding: 0.5rem 0 0.25rem 0; }
.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--violet-2);
    background: rgba(139,92,246,0.12);
    border: 1px solid rgba(139,92,246,0.3);
    padding: 0.3rem 0.8rem;
    border-radius: 100px;
    margin-bottom: 1rem;
}
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(2.2rem, 5vw, 3.75rem);
    font-weight: 800;
    letter-spacing: -0.02em;
    line-height: 1.08;
    margin: 0;
    background: linear-gradient(135deg, #ffffff 10%, var(--violet-2) 55%, var(--cyan) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-sub {
    font-family: 'Inter', sans-serif;
    font-size: 0.95rem;
    color: var(--text-dim);
    margin-top: 0.6rem;
    font-weight: 400;
}

/* ── Cards (glass) ── */
.card {
    background: linear-gradient(145deg, rgba(255,255,255,0.045), rgba(255,255,255,0.015));
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.25s ease, transform 0.25s ease, box-shadow 0.25s ease;
}

.card:hover {
    border-color: var(--border-hover);
    transform: translateY(-2px);
    box-shadow: 0 12px 40px rgba(139,92,246,0.12);
}

.card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 2px;
    background: linear-gradient(90deg, var(--violet), var(--fuchsia), var(--cyan));
    opacity: 0.85;
}

.card-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.13em;
    text-transform: uppercase;
    color: var(--text-dim);
    margin-bottom: 0.85rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.card-content {
    font-size: 0.92rem;
    line-height: 1.75;
    color: var(--text);
    font-family: 'Inter', sans-serif;
}

/* ── Accent Badge ── */
.badge {
    display: inline-block;
    padding: 0.28rem 0.75rem;
    border-radius: 100px;
    font-size: 0.66rem;
    font-weight: 600;
    letter-spacing: 0.09em;
    text-transform: uppercase;
}

.badge-purple { background: rgba(139,92,246,0.16); color: var(--violet-2); border: 1px solid rgba(139,92,246,0.35); }
.badge-cyan   { background: rgba(34,211,238,0.14); color: var(--cyan);    border: 1px solid rgba(34,211,238,0.32); }
.badge-green  { background: rgba(52,211,153,0.14); color: var(--success); border: 1px solid rgba(52,211,153,0.32); }
.badge-pink   { background: rgba(232,121,249,0.14); color: var(--fuchsia); border: 1px solid rgba(232,121,249,0.32); }

/* ── Input & Buttons ── */
.stTextInput > div > div > input,
.stSelectbox > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
}

.stTextInput > div > div > input:focus {
    border-color: var(--violet) !important;
    box-shadow: 0 0 0 3px rgba(139,92,246,0.18) !important;
}

.stButton > button {
    background: linear-gradient(135deg, var(--violet), #6d28d9) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.04em !important;
    padding: 0.65rem 1.5rem !important;
    transition: all 0.2s ease !important;
    text-transform: uppercase !important;
    box-shadow: 0 4px 18px rgba(139,92,246,0.28) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 30px rgba(139,92,246,0.45) !important;
    filter: brightness(1.08);
}

/* Secondary button */
.stButton > button[kind="secondary"] {
    background: rgba(255,255,255,0.045) !important;
    border: 1px solid var(--border) !important;
    box-shadow: none !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: var(--border-hover) !important;
    box-shadow: none !important;
}

/* ── Progress / Status ── */
.status-bar {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.7rem 0.9rem;
    background: rgba(255,255,255,0.035);
    border-radius: var(--radius-sm);
    margin: 0.4rem 0;
    border: 1px solid var(--border);
    font-size: 0.78rem;
    transition: border-color 0.2s ease;
}

.status-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
}

.dot-active   { background: var(--violet-2); box-shadow: 0 0 10px var(--violet-2); animation: pulse 1.4s infinite; }
.dot-done     { background: var(--success); box-shadow: 0 0 8px rgba(52,211,153,0.6); }
.dot-pending  { background: var(--text-faint); }

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%      { opacity: 0.45; transform: scale(0.85); }
}

/* ── Chat ── */
.chat-container {
    background: linear-gradient(145deg, rgba(255,255,255,0.04), rgba(255,255,255,0.015));
    backdrop-filter: blur(18px);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.25rem;
    max-height: 440px;
    overflow-y: auto;
    margin-bottom: 1rem;
}

.chat-msg {
    margin-bottom: 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}

.chat-label {
    font-size: 0.63rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
}

.chat-bubble {
    display: inline-block;
    padding: 0.65rem 1.05rem;
    border-radius: 14px;
    font-size: 0.87rem;
    line-height: 1.65;
    max-width: 90%;
}

.user-label  { color: var(--violet-2); }
.bot-label   { color: var(--cyan); }

.user-bubble {
    background: linear-gradient(135deg, rgba(139,92,246,0.18), rgba(232,121,249,0.1));
    border: 1px solid rgba(139,92,246,0.3);
    align-self: flex-end;
    border-bottom-right-radius: 4px;
}
.bot-bubble  {
    background: rgba(34,211,238,0.08);
    border: 1px solid rgba(34,211,238,0.22);
    align-self: flex-start;
    border-bottom-left-radius: 4px;
}

/* ── Divider ── */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 1.75rem 0 !important;
}

/* ── Transcript box ── */
.transcript-box {
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 1.25rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    line-height: 1.85;
    max-height: 320px;
    overflow-y: auto;
    color: var(--text-dim);
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── Empty state ── */
.empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 5rem 2rem;
    text-align: center;
    background: linear-gradient(145deg, rgba(255,255,255,0.03), rgba(255,255,255,0.008));
    border: 1px dashed var(--border);
    border-radius: 20px;
}
.empty-orb {
    width: 84px; height: 84px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 2.4rem;
    background: radial-gradient(circle at 35% 30%, rgba(139,92,246,0.35), rgba(232,121,249,0.15) 60%, transparent 80%);
    box-shadow: 0 0 60px rgba(139,92,246,0.25);
    margin-bottom: 1.25rem;
}

/* ── Stale Streamlit elements ── */
.stProgress > div > div > div { background: linear-gradient(90deg, var(--violet), var(--fuchsia)) !important; }
.stSpinner > div { border-top-color: var(--violet) !important; }
[data-testid="stMarkdownContainer"] p { color: var(--text) !important; }
label { color: var(--text-dim) !important; font-size: 0.8rem !important; font-weight: 500 !important; }

/* scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--violet); }
</style>
""", unsafe_allow_html=True)

# ─── Session State Init ──────────────────────────────────────────────────────────
for key, default in {
    "result": None,
    "chat_history": [],
    "processing": False,
    "pipeline_done": False,
    "pipeline_steps": {},
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ─── Helpers ────────────────────────────────────────────────────────────────────
def step_status(steps: dict, key: str) -> str:
    s = steps.get(key, "pending")
    if s == "active":  return "dot-active"
    if s == "done":    return "dot-done"
    return "dot-pending"

def render_step_bar(label: str, key: str, icon: str):
    css = step_status(st.session_state.pipeline_steps, key)
    st.markdown(f"""
    <div class="status-bar">
        <div class="status-dot {css}"></div>
        <span>{icon} {label}</span>
    </div>""", unsafe_allow_html=True)

# ─── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="brand-mark">
        <div class="brand-icon">🪐</div>
        <div class="brand-name">VideoVerse-AI</div>
    </div>
    <div class="brand-tag">Meeting Intelligence</div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown('<span class="badge badge-purple">Input</span>', unsafe_allow_html=True)
    source = st.text_input("YouTube URL or File Path", placeholder="https://youtube.com/watch?v=... or /path/to/file.mp4")

    language = st.selectbox("Language", ["english", "hinglish"], index=0)

    run_btn = st.button("⚡  Analyse", use_container_width=True)

    if st.session_state.pipeline_done:
        st.markdown("---")
        st.markdown('<span class="badge badge-green">Pipeline Status</span>', unsafe_allow_html=True)
        for step, icon, label in [
            ("audio",      "🔊", "Audio Processing"),
            ("transcript", "📝", "Transcription"),
            ("title",      "🏷️", "Title Generation"),
            ("summary",    "📋", "Summarisation"),
            ("extract",    "🔍", "Extraction"),
            ("rag",        "🧠", "RAG Engine"),
        ]:
            render_step_bar(label, step, icon)

# ─── Main Area ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-eyebrow">🪐 VideoVerse-AI</div>
    <div class="hero-title">Your meetings,<br>understood instantly.</div>
    <div class="hero-sub">Transcribe · Summarise · Chat with your meetings — all in one place.</div>
</div>
""", unsafe_allow_html=True)
st.markdown("---")

# ── Run Pipeline ────────────────────────────────────────────────────────────────
if run_btn:
    if not source.strip():
        st.error("Please enter a YouTube URL or file path.")
    else:
        st.session_state.pipeline_done = False
        st.session_state.result = None
        st.session_state.chat_history = []
        st.session_state.pipeline_steps = {}

        progress_placeholder = st.empty()

        def update_step(key, state):
            st.session_state.pipeline_steps[key] = state

        try:
            with progress_placeholder.container():
                st.info("⚙️ Pipeline running — see sidebar for live status…")

            update_step("audio", "active")
            chunks = process_input(source)
            update_step("audio", "done")

            update_step("transcript", "active")
            transcript = transcribe_all(chunks, language)
            update_step("transcript", "done")

            update_step("title", "active")
            title = generate_title(transcript)
            update_step("title", "done")

            update_step("summary", "active")
            summary = summarize(transcript)
            update_step("summary", "done")

            update_step("extract", "active")
            action_items  = extract_action_items(transcript)
            decisions     = extract_key_decisions(transcript)
            questions     = extract_questions(transcript)
            update_step("extract", "done")

            update_step("rag", "active")
            rag_chain = build_rag_chain(transcript)
            update_step("rag", "done")

            st.session_state.result = {
                "title": title,
                "transcript": transcript,
                "summary": summary,
                "action_items": action_items,
                "key_decisions": decisions,
                "open_questions": questions,
                "rag_chain": rag_chain,
            }
            st.session_state.pipeline_done = True
            progress_placeholder.success("✅ Analysis complete!")
            time.sleep(0.5)
            progress_placeholder.empty()
            st.rerun()

        except Exception as e:
            for k in ["audio","transcript","title","summary","extract","rag"]:
                if st.session_state.pipeline_steps.get(k) == "active":
                    st.session_state.pipeline_steps[k] = "pending"
            progress_placeholder.error(f"❌ Error: {e}")

# ── Results ──────────────────────────────────────────────────────────────────────
if st.session_state.result:
    r = st.session_state.result

    # Title banner
    st.markdown(f"""
    <div class="card">
        <div class="card-title">📌 Session Title</div>
        <div style="font-family:'Space Grotesk',sans-serif;font-size:1.45rem;font-weight:700;color:var(--text)">
            {r['title']}
        </div>
    </div>""", unsafe_allow_html=True)

    # Top row: summary + transcript
    col1, col2 = st.columns([3, 2], gap="medium")

    with col1:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">📋 Summary</div>
            <div class="card-content">{r['summary']}</div>
        </div>""", unsafe_allow_html=True)

    with col2:
        with st.expander("📝 Full Transcript", expanded=False):
            st.markdown(f'<div class="transcript-box">{r["transcript"]}</div>', unsafe_allow_html=True)

    # Second row: action items | decisions | questions
    c1, c2, c3 = st.columns(3, gap="medium")

    with c1:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">✅ Action Items</div>
            <div class="card-content">{r['action_items']}</div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">🔑 Key Decisions</div>
            <div class="card-content">{r['key_decisions']}</div>
        </div>""", unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">❓ Open Questions</div>
            <div class="card-content">{r['open_questions']}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # ── RAG Chat ──────────────────────────────────────────────────────────────
    st.markdown('<div style="font-family:\'Space Grotesk\',sans-serif;font-size:1.25rem;font-weight:700;margin-bottom:1rem">💬 Chat with your Meeting</div>', unsafe_allow_html=True)

    # Chat history display
    if st.session_state.chat_history:
        chat_html = '<div class="chat-container">'
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                chat_html += f"""
                <div class="chat-msg" style="align-items:flex-end">
                    <span class="chat-label user-label">You</span>
                    <div class="chat-bubble user-bubble">{msg['content']}</div>
                </div>"""
            else:
                chat_html += f"""
                <div class="chat-msg" style="align-items:flex-start">
                    <span class="chat-label bot-label">🪐 VideoVerse-AI</span>
                    <div class="chat-bubble bot-bubble">{msg['content']}</div>
                </div>"""
        chat_html += '</div>'
        st.markdown(chat_html, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="card" style="text-align:center;padding:2rem">
            <div style="font-size:2rem;margin-bottom:0.5rem">💬</div>
            <div style="color:var(--text-dim);font-size:0.85rem">Ask anything about your meeting transcript</div>
        </div>""", unsafe_allow_html=True)

    # Chat input
    chat_col1, chat_col2 = st.columns([5, 1], gap="small")
    with chat_col1:
        user_input = st.text_input("Your question", placeholder="What were the main decisions made?", label_visibility="collapsed")
    with chat_col2:
        send_btn = st.button("Send →", use_container_width=True)

    if send_btn and user_input.strip():
        with st.spinner("Thinking…"):
            answer = ask_question(r["rag_chain"], user_input.strip())
        st.session_state.chat_history.append({"role": "user",      "content": user_input.strip()})
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()

    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat", type="secondary"):
            st.session_state.chat_history = []
            st.rerun()

else:
    # Empty state
    st.markdown("""
    <div class="empty-state">
        <div class="empty-orb">🪐</div>
        <div style="font-family:'Space Grotesk',sans-serif;font-size:1.6rem;font-weight:700;color:var(--text);margin-bottom:0.5rem">
            Ready to Explore Your Meeting
        </div>
        <div style="color:var(--text-dim);font-size:0.88rem;max-width:400px;line-height:1.75">
            Paste a YouTube URL or local file path in the sidebar, choose your language, and hit <strong style="color:var(--violet-2)">Analyse</strong> to get started.
        </div>
        <div style="margin-top:2rem;display:flex;gap:0.6rem;flex-wrap:wrap;justify-content:center">
            <span class="badge badge-purple">Transcription</span>
            <span class="badge badge-cyan">Summarisation</span>
            <span class="badge badge-pink">RAG Chat</span>
        </div>
    </div>""", unsafe_allow_html=True)