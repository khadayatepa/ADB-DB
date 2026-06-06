import streamlit as st
import json
import random
import time
from pathlib import Path

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="1Z0-931-25 · Oracle ADB Exam Trainer",
    page_icon="🔴",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── Load questions ────────────────────────────────────────────────────────────
@st.cache_data
def load_questions():
    p = Path(__file__).parent / "questions.json"
    return json.loads(p.read_text())

ALL_Q = load_questions()

# ── Custom CSS (light theme, Oracle palette) ──────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ── Root overrides ── */
html, body, [class*="css"] {
    font-family: 'Syne', sans-serif !important;
    background-color: #f8f9fb !important;
    color: #1e2433 !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #e5e9f0 !important;
}
[data-testid="stSidebar"] * { color: #1e2433 !important; }

/* ── Remove default top padding ── */
.block-container { padding-top: 1.5rem !important; max-width: 820px !important; }

/* ── Hero banner ── */
.hero-banner {
    background: linear-gradient(135deg, #c74634 0%, #e85d04 50%, #f48c06 100%);
    border-radius: 14px;
    padding: 24px 28px;
    margin-bottom: 20px;
    color: white;
    position: relative;
    overflow: hidden;
}
.hero-banner::after {
    content: 'ADB';
    position: absolute; right: 24px; top: 50%;
    transform: translateY(-50%);
    font-family: 'JetBrains Mono', monospace;
    font-size: 5rem; font-weight: 800;
    opacity: 0.12; letter-spacing: -4px;
}
.hero-title {
    font-size: 1.55rem; font-weight: 800;
    letter-spacing: -0.02em; margin: 0 0 4px;
    color: white;
}
.hero-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem; letter-spacing: 0.12em;
    text-transform: uppercase; opacity: 0.85;
    color: white; margin: 0;
}

/* ── Stats row ── */
.stats-row {
    display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap;
}
.stat-chip {
    flex: 1; min-width: 80px;
    background: #ffffff;
    border: 1px solid #e5e9f0;
    border-radius: 10px;
    padding: 12px 14px; text-align: center;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
.stat-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.6rem; font-weight: 700;
    line-height: 1; margin-bottom: 2px;
}
.stat-lbl { font-size: 0.68rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.06em; }
.stat-num.orange { color: #e85d04; }
.stat-num.green  { color: #059669; }
.stat-num.red    { color: #dc2626; }
.stat-num.blue   { color: #2563eb; }

/* ── Question card ── */
.q-card {
    background: #ffffff;
    border: 1px solid #e5e9f0;
    border-radius: 14px;
    padding: 24px 26px;
    margin-bottom: 16px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}
.q-meta {
    display: flex; align-items: center; gap: 8px; margin-bottom: 14px;
}
.q-num-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem; font-weight: 600; color: #e85d04;
    background: #fff4ee; border: 1px solid #fdd5b5;
    padding: 3px 9px; border-radius: 5px; letter-spacing: 0.06em;
}
.q-type-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.63rem; letter-spacing: 0.06em; text-transform: uppercase;
    padding: 3px 9px; border-radius: 5px;
}
.badge-single { background: #eff6ff; color: #2563eb; border: 1px solid #bfdbfe; }
.badge-multi  { background: #fffbeb; color: #d97706; border: 1px solid #fde68a; }
.q-text {
    font-size: 1.0rem; line-height: 1.7; color: #1e2433;
    margin: 0; font-weight: 500;
}

/* ── Option buttons ── */
div[data-testid="stRadio"] > label,
div[data-testid="stCheckbox"] > label {
    background: #f8f9fb !important;
    border: 1.5px solid #e5e9f0 !important;
    border-radius: 9px !important;
    padding: 10px 14px !important;
    margin-bottom: 6px !important;
    cursor: pointer !important;
    transition: border-color 0.15s !important;
    display: flex !important;
    font-size: 0.88rem !important;
}
div[data-testid="stRadio"] > label:hover,
div[data-testid="stCheckbox"] > label:hover {
    border-color: #e85d04 !important;
    background: #fff8f5 !important;
}

/* ── Feedback boxes ── */
.fb-correct {
    background: #f0fdf4; border-left: 4px solid #059669;
    border-radius: 0 10px 10px 0; padding: 12px 16px;
    margin: 12px 0;
}
.fb-wrong {
    background: #fef2f2; border-left: 4px solid #dc2626;
    border-radius: 0 10px 10px 0; padding: 12px 16px;
    margin: 12px 0;
}
.fb-label { font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.08em;
    text-transform: uppercase; margin-bottom: 5px; }
.fb-correct .fb-label { color: #059669; }
.fb-wrong   .fb-label { color: #dc2626; }
.fb-text { font-size: 0.85rem; line-height: 1.6; color: #374151; }

/* ── Correct answer display ── */
.correct-ans {
    background: #eff6ff; border: 1px solid #bfdbfe;
    border-radius: 8px; padding: 8px 14px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem; color: #1d4ed8;
    margin-bottom: 12px;
}

/* ── Score card ── */
.score-card {
    background: #ffffff; border: 1px solid #e5e9f0;
    border-radius: 16px; padding: 32px 28px;
    text-align: center; margin-bottom: 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.07);
}
.score-pct {
    font-size: 5rem; font-weight: 800; line-height: 1;
    background: linear-gradient(135deg, #c74634, #f48c06);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
}
.score-verdict { font-size: 1.3rem; font-weight: 700; margin-bottom: 4px; }
.score-detail {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem; color: #64748b;
}

/* ── Review row ── */
.rev-row {
    display: flex; align-items: flex-start; gap: 10px;
    padding: 10px 14px; border-radius: 9px;
    border: 1px solid #e5e9f0; margin-bottom: 6px;
    background: #fff;
}
.rev-row.ok  { border-color: #bbf7d0; background: #f0fdf4; }
.rev-row.bad { border-color: #fecaca; background: #fef2f2; }
.rev-icon { font-size: 1rem; flex-shrink: 0; margin-top: 1px; }
.rev-qtext { flex: 1; font-size: 0.82rem; color: #374151; line-height: 1.5; }
.rev-ans {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem; text-align: right; flex-shrink: 0;
}
.rev-correct { color: #059669; font-weight: 600; }
.rev-yours   { color: #dc2626; }

/* ── Progress bar ── */
.stProgress > div > div { background: linear-gradient(90deg, #e85d04, #f48c06) !important; }

/* ── Buttons ── */
.stButton > button {
    background: #e85d04 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.03em !important;
    padding: 0.45rem 1.2rem !important;
    transition: all 0.15s !important;
}
.stButton > button:hover {
    background: #c74634 !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(232,93,4,0.3) !important;
}
.stButton > button[kind="secondary"] {
    background: #f1f5f9 !important;
    color: #475569 !important;
    border: 1px solid #e5e9f0 !important;
}
.stButton > button[kind="secondary"]:hover {
    background: #e2e8f0 !important;
    transform: none !important;
    box-shadow: none !important;
}

/* ── Divider ── */
hr { border-color: #e5e9f0 !important; margin: 16px 0 !important; }

/* ── Mode selector ── */
div[data-testid="stSelectbox"] > div {
    border-radius: 9px !important;
    border-color: #e5e9f0 !important;
}

/* ── Hide streamlit branding ── */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Session state init ────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "mode": "Practice",
        "order": [],
        "current": 0,
        "answers": {},      # {idx: list of letters}
        "submitted": set(), # set of idx
        "show_score": False,
        "mock_submitted": False,
        "filter_type": "All",
        "search": "",
        "initialized": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ── Helpers ───────────────────────────────────────────────────────────────────
def get_filtered():
    ft = st.session_state.filter_type
    s  = st.session_state.search.lower()
    out = []
    for q in ALL_Q:
        type_ok = (ft == "All") or (ft == "Single Answer" and not q["multi"]) or (ft == "Multi-Select" and q["multi"])
        text_ok = not s or s in q["question"].lower() or any(s in o.lower() for o in q["options"])
        if type_ok and text_ok:
            out.append(q)
    return out

def reset_quiz(shuffle=False):
    filtered = get_filtered()
    order = list(range(len(filtered)))
    if shuffle:
        random.shuffle(order)
    st.session_state.order    = order
    st.session_state.current  = 0
    st.session_state.answers  = {}
    st.session_state.submitted = set()
    st.session_state.show_score = False
    st.session_state.mock_submitted = False
    st.session_state.filtered_questions = filtered

def is_correct(idx):
    q   = st.session_state.filtered_questions[st.session_state.order[idx]]
    sel = set(st.session_state.answers.get(idx, []))
    return sel == set(q["answer"])

# ── Init on first load ────────────────────────────────────────────────────────
if not st.session_state.initialized:
    reset_quiz()
    st.session_state.initialized = True

filtered_qs = get_filtered() if not hasattr(st.session_state, "filtered_questions") else st.session_state.get("filtered_questions", get_filtered())

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    mode = st.selectbox(
        "Mode",
        ["Practice", "Mock Exam", "Review All"],
        index=["Practice", "Mock Exam", "Review All"].index(st.session_state.mode),
        key="mode_select"
    )
    if mode != st.session_state.mode:
        st.session_state.mode = mode
        reset_quiz()
        st.rerun()

    st.markdown("---")
    st.markdown("### 🔍 Filter")
    
    ft = st.selectbox(
        "Question Type",
        ["All", "Single Answer", "Multi-Select"],
        index=["All", "Single Answer", "Multi-Select"].index(st.session_state.filter_type),
    )
    if ft != st.session_state.filter_type:
        st.session_state.filter_type = ft
        reset_quiz()
        st.rerun()

    search = st.text_input("Search", value=st.session_state.search, placeholder="keyword...")
    if search != st.session_state.search:
        st.session_state.search = search
        reset_quiz()
        st.rerun()

    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔀 Shuffle", use_container_width=True):
            reset_quiz(shuffle=True)
            st.rerun()
    with col2:
        if st.button("↺ Reset", use_container_width=True):
            reset_quiz()
            st.rerun()

    st.markdown("---")
    st.markdown("### 📊 Session Stats")
    filtered = get_filtered()
    total    = len(filtered)
    answered = len(st.session_state.submitted)
    correct  = sum(1 for i in st.session_state.submitted if is_correct(i)) if st.session_state.submitted and hasattr(st.session_state, "filtered_questions") else 0

    st.markdown(f"""
    <div style='font-family:"JetBrains Mono",monospace;font-size:0.78rem;line-height:2;color:#374151'>
    📚 Total: <b style='color:#e85d04'>{total}</b><br>
    ✅ Correct: <b style='color:#059669'>{correct}</b><br>
    ❌ Wrong: <b style='color:#dc2626'>{answered - correct}</b><br>
    ⏭️ Remaining: <b style='color:#2563eb'>{total - answered}</b>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        "<p style='font-size:0.68rem;color:#94a3b8;font-family:JetBrains Mono,monospace;"
        "text-align:center'>1Z0-931-25 · Oracle ADB<br>141 Questions</p>",
        unsafe_allow_html=True
    )

# ── MAIN AREA ─────────────────────────────────────────────────────────────────

# Hero
st.markdown("""
<div class="hero-banner">
  <p class="hero-sub">Oracle Autonomous Database Cloud 2025 Professional</p>
  <h1 class="hero-title">1Z0-931-25 Exam Trainer</h1>
</div>
""", unsafe_allow_html=True)

# Stats row
filtered = get_filtered()
total    = len(filtered)
answered = len(st.session_state.submitted) if st.session_state.submitted else 0
correct  = sum(1 for i in st.session_state.submitted if is_correct(i)) if st.session_state.submitted and hasattr(st.session_state, "filtered_questions") else 0
wrong    = answered - correct
remaining = total - answered

st.markdown(f"""
<div class="stats-row">
  <div class="stat-chip">
    <div class="stat-num orange">{total}</div>
    <div class="stat-lbl">Questions</div>
  </div>
  <div class="stat-chip">
    <div class="stat-num green">{correct}</div>
    <div class="stat-lbl">Correct</div>
  </div>
  <div class="stat-chip">
    <div class="stat-num red">{wrong}</div>
    <div class="stat-lbl">Wrong</div>
  </div>
  <div class="stat-chip">
    <div class="stat-num blue">{remaining}</div>
    <div class="stat-lbl">Remaining</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Guard: no questions
if not total:
    st.warning("No questions match your current filter. Try changing the filter settings in the sidebar.")
    st.stop()

# Ensure filtered_questions is up to date
if not hasattr(st.session_state, "filtered_questions") or len(st.session_state.get("filtered_questions", [])) != total:
    reset_quiz()
    st.rerun()

fq = st.session_state.filtered_questions
order = st.session_state.order

# ── REVIEW ALL MODE ───────────────────────────────────────────────────────────
if st.session_state.mode == "Review All":
    st.markdown(f"### 📖 All Questions ({total})")
    for pos, oidx in enumerate(order):
        q = fq[oidx]
        badge = "badge-multi" if q["multi"] else "badge-single"
        btext = f"MULTI-SELECT · {len(q['answer'])} correct" if q["multi"] else "SINGLE ANSWER"
        st.markdown(f"""
        <div class="q-card">
          <div class="q-meta">
            <span class="q-num-badge">Q{q['num']}</span>
            <span class="q-type-badge {badge}">{btext}</span>
          </div>
          <p class="q-text">{q['question']}</p>
        </div>
        """, unsafe_allow_html=True)
        correct_letters = set(q["answer"])
        for opt in q["options"]:
            letter = opt[0]
            is_c = letter in correct_letters
            icon  = "✅" if is_c else "○"
            color = "#059669" if is_c else "#94a3b8"
            fw    = "700" if is_c else "400"
            st.markdown(
                f"<div style='padding:8px 12px;margin-bottom:4px;border-radius:7px;"
                f"background:{'#f0fdf4' if is_c else '#f8f9fb'};"
                f"border:1px solid {'#bbf7d0' if is_c else '#e5e9f0'};"
                f"font-size:0.88rem;color:{color};font-weight:{fw}'>"
                f"{icon} {opt[3:]}</div>",
                unsafe_allow_html=True
            )
        if q.get("explanation"):
            st.markdown(
                f"<div class='fb-correct' style='margin-top:8px'>"
                f"<div class='fb-label'>Explanation</div>"
                f"<div class='fb-text'>{q['explanation']}</div></div>",
                unsafe_allow_html=True
            )
        st.markdown("<hr>", unsafe_allow_html=True)
    st.stop()

# ── SCORE SCREEN ──────────────────────────────────────────────────────────────
if st.session_state.show_score:
    pct     = round(correct / total * 100) if total else 0
    verdict = ("🎉 Pass Ready!" if pct >= 80 else "📚 Almost There" if pct >= 65 else "🔁 Keep Studying")
    vcolor  = ("#059669" if pct >= 80 else "#d97706" if pct >= 65 else "#dc2626")

    st.markdown(f"""
    <div class="score-card">
      <div class="score-pct">{pct}%</div>
      <div class="score-verdict" style="color:{vcolor}">{verdict}</div>
      <div class="score-detail">{correct} of {total} correct &nbsp;·&nbsp; {answered} attempted &nbsp;·&nbsp; {total - answered} skipped</div>
    </div>
    """, unsafe_allow_html=True)

    # stat chips
    st.markdown(f"""
    <div class="stats-row">
      <div class="stat-chip"><div class="stat-num green">{correct}</div><div class="stat-lbl">Correct</div></div>
      <div class="stat-chip"><div class="stat-num red">{wrong}</div><div class="stat-lbl">Wrong</div></div>
      <div class="stat-chip"><div class="stat-num blue">{total - answered}</div><div class="stat-lbl">Skipped</div></div>
      <div class="stat-chip"><div class="stat-num orange">{total}</div><div class="stat-lbl">Total</div></div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        if st.button("🔀 Retry Shuffled", use_container_width=True):
            reset_quiz(shuffle=True)
            st.rerun()
    with c2:
        if st.button("↺ Retry Same Order", use_container_width=True):
            reset_quiz()
            st.rerun()
    with c3:
        if st.button("📖 Review Answers", use_container_width=True):
            st.session_state.mode = "Review All"
            reset_quiz()
            st.rerun()

    st.markdown("---")
    st.markdown("### 📋 Review Summary")
    for pos, oidx in enumerate(order):
        ok  = pos in st.session_state.submitted and is_correct(pos)
        q   = fq[oidx]
        sel = st.session_state.answers.get(pos, [])
        sel_str = ", ".join(sorted(sel)) if sel else "—"
        row_cls = "ok" if ok else "bad"
        icon    = "✅" if ok else "❌"
        ans_html = f'<span class="rev-correct">{", ".join(sorted(q["answer"]))}</span>'
        if not ok and sel:
            ans_html += f' / <span class="rev-yours">{sel_str}</span>'
        st.markdown(f"""
        <div class="rev-row {row_cls}">
          <span class="rev-icon">{icon}</span>
          <span class="rev-qtext"><b>Q{q['num']}.</b> {q['question'][:80]}{'…' if len(q['question'])>80 else ''}</span>
          <span class="rev-ans">{ans_html}</span>
        </div>
        """, unsafe_allow_html=True)
    st.stop()

# ── QUESTION VIEW ─────────────────────────────────────────────────────────────
cur = st.session_state.current
if cur >= len(order):
    st.session_state.show_score = True
    st.rerun()

q    = fq[order[cur]]
is_submitted_cur = cur in st.session_state.submitted

# Progress bar
progress_val = (cur + 1) / total
st.progress(progress_val)
st.markdown(
    f"<p style='text-align:right;font-family:JetBrains Mono,monospace;font-size:0.72rem;"
    f"color:#64748b;margin-top:-8px'>Q {cur+1} / {total}</p>",
    unsafe_allow_html=True
)

# Question card header
badge_cls  = "badge-multi" if q["multi"] else "badge-single"
badge_text = f"MULTI-SELECT · Choose {len(q['answer'])}" if q["multi"] else "SINGLE ANSWER"

st.markdown(f"""
<div class="q-card">
  <div class="q-meta">
    <span class="q-num-badge">Q{q['num']}</span>
    <span class="q-type-badge {badge_cls}">{badge_text}</span>
  </div>
  <p class="q-text">{q['question']}</p>
</div>
""", unsafe_allow_html=True)

# Options
option_labels = [o[3:] for o in q["options"]]  # strip "A. "
option_keys   = [o[0]  for o in q["options"]]  # ["A","B","C",...]
full_options  = [f"{k}. {v}" for k, v in zip(option_keys, option_labels)]

if q["multi"]:
    current_sel = st.session_state.answers.get(cur, [])
    chosen = st.multiselect(
        "Select all correct answers:",
        full_options,
        default=[f"{k}. {option_labels[i]}" for i, k in enumerate(option_keys) if k in current_sel],
        disabled=is_submitted_cur,
        key=f"ms_{cur}_{q['num']}",
        label_visibility="visible"
    )
    chosen_letters = [c.split(".")[0].strip() for c in chosen]
else:
    current_sel = st.session_state.answers.get(cur, [])
    default_idx = None
    if current_sel:
        try:
            default_idx = option_keys.index(current_sel[0])
        except ValueError:
            default_idx = None
    chosen_radio = st.radio(
        "Select the correct answer:",
        full_options,
        index=default_idx,
        disabled=is_submitted_cur,
        key=f"r_{cur}_{q['num']}",
        label_visibility="visible"
    )
    chosen_letters = [chosen_radio.split(".")[0].strip()] if chosen_radio else []

# Save selection live
if not is_submitted_cur:
    st.session_state.answers[cur] = chosen_letters

# ── PRACTICE MODE: submit + feedback ──────────────────────────────────────────
if st.session_state.mode == "Practice":

    if not is_submitted_cur:
        col_sub, col_skip = st.columns([2, 1])
        with col_sub:
            sub_disabled = not chosen_letters
            if st.button("✔ Check Answer", disabled=sub_disabled, use_container_width=True):
                st.session_state.submitted.add(cur)
                st.rerun()
        with col_skip:
            if st.button("Skip →", use_container_width=True):
                st.session_state.current = cur + 1
                st.rerun()
    else:
        ok = is_correct(cur)
        correct_letters = set(q["answer"])
        user_letters    = set(st.session_state.answers.get(cur, []))

        # Show correct answer first
        st.markdown(
            f"<div class='correct-ans'>✔ Correct Answer: <b>{', '.join(sorted(correct_letters))}</b></div>",
            unsafe_allow_html=True
        )

        if ok:
            st.markdown(
                f"<div class='fb-correct'>"
                f"<div class='fb-label'>✓ Correct!</div>"
                f"<div class='fb-text'>{q.get('explanation','')}</div></div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div class='fb-wrong'>"
                f"<div class='fb-label'>✗ Incorrect — You chose: {', '.join(sorted(user_letters)) or '—'}</div>"
                f"<div class='fb-text'>{q.get('explanation','')}</div></div>",
                unsafe_allow_html=True
            )

        col_prev, col_next = st.columns([1, 2])
        with col_prev:
            if cur > 0:
                if st.button("← Prev", use_container_width=True):
                    st.session_state.current = cur - 1
                    st.rerun()
        with col_next:
            is_last = cur >= total - 1
            label = "🏁 View Score" if is_last else "Next →"
            if st.button(label, use_container_width=True):
                if is_last:
                    st.session_state.show_score = True
                else:
                    st.session_state.current = cur + 1
                st.rerun()

# ── MOCK EXAM MODE ─────────────────────────────────────────────────────────────
elif st.session_state.mode == "Mock Exam":
    nav_col1, nav_col2, nav_col3 = st.columns([1, 1, 1])
    with nav_col1:
        if st.button("← Previous", disabled=(cur == 0), use_container_width=True):
            st.session_state.current = cur - 1
            st.rerun()
    with nav_col2:
        ans_count = len(st.session_state.answers)
        st.markdown(
            f"<p style='text-align:center;font-family:JetBrains Mono,monospace;"
            f"font-size:0.75rem;color:#64748b;margin-top:8px'>{ans_count}/{total} answered</p>",
            unsafe_allow_html=True
        )
    with nav_col3:
        if cur < total - 1:
            if st.button("Next →", use_container_width=True):
                st.session_state.current = cur + 1
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📋 Submit Mock Exam", use_container_width=True):
        # Mark all answered as submitted
        for i, ans in st.session_state.answers.items():
            if ans:
                st.session_state.submitted.add(i)
        st.session_state.show_score = True
        st.rerun()
