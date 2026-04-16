import streamlit as st
import time
import sys
import os

# Add the Multi_Agent directory to path so we can import from it
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pipeline import run_research_pipeline

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:ital,wght@0,400;0,500;1,400&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Root & body ── */
:root {
    --bg:        #0a0b0e;
    --surface:   #111318;
    --border:    #1e2028;
    --accent:    #00e5c0;
    --accent2:   #ff6b35;
    --accent3:   #a259ff;
    --text:      #e8eaf0;
    --muted:     #5a5f72;
    --success:   #00c96f;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(0,229,192,0.07) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 90% 80%, rgba(162,89,255,0.05) 0%, transparent 50%),
        var(--bg) !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
.block-container { padding: 2.5rem 3rem 4rem !important; max-width: 1100px !important; }

/* ── Typography ── */
h1, h2, h3, h4 { font-family: 'Syne', sans-serif !important; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3.5rem 0 2.5rem;
    position: relative;
}
.hero-badge {
    display: inline-block;
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--accent);
    border: 1px solid rgba(0,229,192,0.3);
    border-radius: 100px;
    padding: 0.35rem 1rem;
    margin-bottom: 1.2rem;
    background: rgba(0,229,192,0.05);
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.2rem, 5vw, 3.6rem);
    font-weight: 800;
    line-height: 1.1;
    background: linear-gradient(135deg, #fff 0%, var(--accent) 60%, var(--accent3) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.8rem;
}
.hero-sub {
    color: var(--muted);
    font-size: 1rem;
    font-weight: 300;
    max-width: 520px;
    margin: 0 auto 2.5rem;
    line-height: 1.7;
}

/* ── Agent pipeline strip ── */
.pipeline-strip {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0;
    margin-bottom: 3rem;
    flex-wrap: wrap;
}
.agent-node {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.4rem;
}
.agent-icon {
    width: 48px; height: 48px;
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.3rem;
    border: 1px solid var(--border);
    background: var(--surface);
}
.agent-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.62rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: var(--muted);
}
.pipeline-arrow {
    width: 36px;
    height: 2px;
    background: linear-gradient(90deg, var(--border), rgba(0,229,192,0.4), var(--border));
    position: relative;
    margin: 0 4px;
    margin-bottom: 24px;
}
.pipeline-arrow::after {
    content: '';
    position: absolute;
    right: -1px; top: -3px;
    border: 4px solid transparent;
    border-left-color: rgba(0,229,192,0.4);
}

/* ── Search input ── */
.stTextInput > div > div > input {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.85rem 1.2rem !important;
    transition: border-color 0.2s !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(0,229,192,0.1) !important;
}
.stTextInput > div > div > input::placeholder { color: var(--muted) !important; }
.stTextInput label { color: var(--muted) !important; font-size: 0.78rem !important; letter-spacing: 0.06em !important; text-transform: uppercase !important; font-family: 'DM Mono', monospace !important; }

/* ── Button ── */
.stButton > button {
    background: var(--accent) !important;
    color: #000 !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 2rem !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.03em !important;
}
.stButton > button:hover {
    background: #00ffda !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(0,229,192,0.25) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Step cards ── */
.step-card {
    border: 1px solid var(--border);
    border-radius: 16px;
    background: var(--surface);
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s;
}
.step-card.active  { border-color: rgba(0,229,192,0.5); }
.step-card.done    { border-color: rgba(0,201,111,0.4); }
.step-card.pending { opacity: 0.45; }

.step-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: transparent;
    transition: background 0.3s;
}
.step-card.active::before  { background: linear-gradient(90deg, var(--accent), var(--accent3)); }
.step-card.done::before    { background: var(--success); }

.step-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.5rem;
}
.step-num {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: var(--muted);
    background: rgba(255,255,255,0.04);
    border-radius: 6px;
    padding: 0.2rem 0.5rem;
    border: 1px solid var(--border);
}
.step-title {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    color: var(--text);
}
.step-status {
    margin-left: auto;
    font-size: 0.75rem;
    font-family: 'DM Mono', monospace;
}
.status-active  { color: var(--accent); }
.status-done    { color: var(--success); }
.status-pending { color: var(--muted); }

.step-desc {
    font-size: 0.82rem;
    color: var(--muted);
    line-height: 1.5;
}

/* ── Result sections ── */
.result-section {
    margin-top: 2.5rem;
}
.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.18em;
    color: var(--muted);
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── Content boxes ── */
.content-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.9rem;
    line-height: 1.75;
    color: #c8cad4;
    max-height: 380px;
    overflow-y: auto;
    white-space: pre-wrap;
    word-break: break-word;
}
.content-box::-webkit-scrollbar { width: 4px; }
.content-box::-webkit-scrollbar-track { background: transparent; }
.content-box::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }

/* Report box gets special treatment */
.report-box {
    background: var(--surface);
    border: 1px solid rgba(0,229,192,0.2);
    border-radius: 14px;
    padding: 1.8rem 2rem;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.93rem;
    line-height: 1.8;
    color: var(--text);
    white-space: pre-wrap;
    word-break: break-word;
    position: relative;
}
.report-box::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent3));
    border-radius: 14px 14px 0 0;
}

/* Critic / feedback box */
.feedback-box {
    background: linear-gradient(135deg, rgba(162,89,255,0.06), rgba(255,107,53,0.04));
    border: 1px solid rgba(162,89,255,0.25);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.88rem;
    line-height: 1.75;
    color: #c8cad4;
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── Divider ── */
.fancy-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 2.5rem 0;
}

/* ── Spinner override ── */
[data-testid="stSpinner"] { color: var(--accent) !important; }

/* ── Expander ── */
.streamlit-expanderHeader {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.8rem !important;
    color: var(--muted) !important;
}
.streamlit-expanderContent {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
}

/* ── Toast-like error ── */
.error-box {
    background: rgba(255,60,60,0.08);
    border: 1px solid rgba(255,60,60,0.3);
    border-radius: 12px;
    padding: 1rem 1.4rem;
    font-size: 0.88rem;
    color: #ff8080;
    font-family: 'DM Mono', monospace;
}
</style>
""", unsafe_allow_html=True)


# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">⬡ Autonomous Research Pipeline</div>
    <div class="hero-title">Multi-Agent Research<br>System</div>
    <div class="hero-sub">Four specialised AI agents — Search · Reader · Writer · Critic — collaborate in sequence to produce deep, structured research on any topic.</div>
</div>
""", unsafe_allow_html=True)

# ── Agent pipeline strip ───────────────────────────────────────────────────────
st.markdown("""
<div class="pipeline-strip">
    <div class="agent-node">
        <div class="agent-icon">🔍</div>
        <div class="agent-label">Search</div>
    </div>
    <div class="pipeline-arrow"></div>
    <div class="agent-node">
        <div class="agent-icon">📄</div>
        <div class="agent-label">Reader</div>
    </div>
    <div class="pipeline-arrow"></div>
    <div class="agent-node">
        <div class="agent-icon">✍️</div>
        <div class="agent-label">Writer</div>
    </div>
    <div class="pipeline-arrow"></div>
    <div class="agent-node">
        <div class="agent-icon">🧠</div>
        <div class="agent-label">Critic</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Input row ─────────────────────────────────────────────────────────────────
col_inp, col_btn = st.columns([5, 1.2], gap="medium")
with col_inp:
    topic = st.text_input(
        "Research Topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        label_visibility="visible",
    )
with col_btn:
    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    run_btn = st.button("Run Pipeline →")

st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)

# ── Step status cards ──────────────────────────────────────────────────────────
STEPS = [
    ("01", "Search Agent",  "Queries the web for recent, reliable information on the topic."),
    ("02", "Reader Agent",  "Scrapes the most relevant URL for deeper contextual content."),
    ("03", "Writer Chain",  "Synthesises all research into a structured, readable report."),
    ("04", "Critic Chain",  "Reviews the report for accuracy, gaps, and improvement points."),
]

def render_steps(current: int):
    cols = st.columns(4, gap="small")
    for i, (num, title, desc) in enumerate(STEPS):
        if i < current:
            cls, status_cls, status_txt = "done",    "status-done",    "✓ Done"
        elif i == current:
            cls, status_cls, status_txt = "active",  "status-active",  "⬡ Running"
        else:
            cls, status_cls, status_txt = "pending", "status-pending", "· Pending"

        with cols[i]:
            st.markdown(f"""
            <div class="step-card {cls}">
                <div class="step-header">
                    <span class="step-num">{num}</span>
                    <span class="step-title">{title}</span>
                    <span class="step-status {status_cls}">{status_txt}</span>
                </div>
                <div class="step-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

# ── Session state init ─────────────────────────────────────────────────────────
if "result" not in st.session_state:
    st.session_state.result = None
if "last_topic" not in st.session_state:
    st.session_state.last_topic = ""
if "error" not in st.session_state:
    st.session_state.error = None

# ── Initial idle state ─────────────────────────────────────────────────────────
if not run_btn and st.session_state.result is None:
    render_steps(-1)   # all pending

# ── Run pipeline ───────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.markdown('<div class="error-box">⚠ Please enter a research topic before running the pipeline.</div>', unsafe_allow_html=True)
    else:
        st.session_state.result = None
        st.session_state.error  = None
        st.session_state.last_topic = topic.strip()

        step_placeholder   = st.empty()
        status_placeholder = st.empty()

        try:
            # Step 0 — search
            with step_placeholder.container():
                render_steps(0)
            with status_placeholder.container():
                with st.spinner("Search agent scanning the web…"):
                    from agents import build_search_agent
                    search_agent  = build_search_agent()
                    search_result = search_agent.invoke({
                        "messages": [("user", f"Find recent, reliable and detailed information about: {topic.strip()}")]
                    })
                    search_content = search_result["messages"][-1].content

            # Step 1 — reader
            with step_placeholder.container():
                render_steps(1)
            with status_placeholder.container():
                with st.spinner("Reader agent scraping top resources…"):
                    from agents import build_reader_agent
                    reader_agent  = build_reader_agent()
                    reader_result = reader_agent.invoke({
                        "messages": [("user",
                            f"Based on the following search results about '{topic.strip()}', "
                            f"pick the most relevant URL and scrape it for deeper content.\n\n"
                            f"Search Results:\n{search_content[:800]}"
                        )]
                    })
                    scraped_content = reader_result["messages"][-1].content

            # Step 2 — writer
            with step_placeholder.container():
                render_steps(2)
            with status_placeholder.container():
                with st.spinner("Writer drafting the report…"):
                    from agents import writer_chain
                    research_combined = (
                        f"SEARCH RESULTS:\n{search_content}\n\n"
                        f"DETAILED SCRAPED CONTENT:\n{scraped_content}"
                    )
                    report = writer_chain.invoke({
                        "topic":    topic.strip(),
                        "research": research_combined,
                    })

            # Step 3 — critic
            with step_placeholder.container():
                render_steps(3)
            with status_placeholder.container():
                with st.spinner("Critic reviewing the report…"):
                    from agents import critic_chain
                    feedback = critic_chain.invoke({"report": report})

            # All done
            with step_placeholder.container():
                render_steps(4)
            status_placeholder.empty()

            st.session_state.result = {
                "search_results":  search_content,
                "scraped_content": scraped_content,
                "report":          report,
                "feedback":        feedback,
            }

        except Exception as e:
            st.session_state.error = str(e)
            step_placeholder.empty()
            status_placeholder.empty()

# ── Error display ──────────────────────────────────────────────────────────────
if st.session_state.error:
    st.markdown(f'<div class="error-box">🚨 Pipeline error: {st.session_state.error}</div>', unsafe_allow_html=True)

# ── Results display ────────────────────────────────────────────────────────────
if st.session_state.result:
    r = st.session_state.result

    st.markdown("<div class='fancy-divider'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-family:'Syne',sans-serif;font-size:0.78rem;color:var(--muted,#5a5f72);
                text-transform:uppercase;letter-spacing:0.15em;margin-bottom:1.5rem;">
        Research Results · <span style="color:#00e5c0">{st.session_state.last_topic}</span>
    </div>
    """, unsafe_allow_html=True)

    # — Final Report (prominent) ——————————————————————
    st.markdown('<div class="section-label">Final Report</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="report-box">{r["report"]}</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    # — Critic Feedback ——————————————————————————————
    st.markdown('<div class="section-label">Critic Feedback</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="feedback-box">{r["feedback"]}</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

    # — Raw agent outputs (collapsible) ——————————————
    with st.expander("▸ Raw Search Results"):
        st.markdown(f'<div class="content-box">{r["search_results"]}</div>', unsafe_allow_html=True)

    with st.expander("▸ Scraped Web Content"):
        st.markdown(f'<div class="content-box">{r["scraped_content"]}</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

    # — Download button ——————————————————————————————
    export_text = (
        f"# Research Report: {st.session_state.last_topic}\n\n"
        f"## Report\n{r['report']}\n\n"
        f"## Critic Feedback\n{r['feedback']}\n\n"
        f"---\n## Raw Search Results\n{r['search_results']}\n\n"
        f"## Scraped Content\n{r['scraped_content']}"
    )
    st.download_button(
        label="⬇ Download Full Report (.txt)",
        data=export_text,
        file_name=f"research_{st.session_state.last_topic[:40].replace(' ','_')}.txt",
        mime="text/plain",
    )