# app.py
# MindEase: Mood Journal + Mood Analyzer + Mood History + Self-care Tools + Crisis Support
# Streamlit Cloud friendly (no ngrok, no login)

import os
from datetime import datetime, date

import pandas as pd
import streamlit as st


# ---------- Config ----------
st.set_page_config(page_title="MindEase", layout="centered")

DATA_FILE = "mood_log.csv"

MOODS = [
    "Happy", "Calm", "Okay", "Worried", "Anxious", "Stressed",
    "Sad", "Angry", "Frustrated", "Tired"
]

# For charting: higher = better
MOOD_SCORE = {
    "Happy": 5,
    "Calm": 4,
    "Okay": 3,
    "Worried": 2,
    "Anxious": 2,
    "Stressed": 1,
    "Sad": 1,
    "Angry": 1,
    "Frustrated": 1,
    "Tired": 2,
}

# Broad keyword sets (simple + manageable)
HIGH_DISTRESS_PHRASES = [
    "i want to die", "want to die", "kill myself", "end my life",
    "suicide", "take my life", "don't want to live", "dont want to live",
    "i can't go on", "i cant go on"
]

NEGATIVE_WORDS = [
    "sad", "depressed", "depressing", "hopeless",
    "stressed", "stress", "overwhelmed", "anxious", "anxiety",
    "angry", "mad", "furious", "frustrated", "worried", "panic",
    "tired", "exhausted", "burnt out", "burned out", "lonely"
]

POSITIVE_WORDS = [
    "happy", "good", "great", "calm", "relaxed", "fine",
    "better", "excited", "motivated", "hopeful", "grateful"
]


# ---------- Helpers ----------
def load_log() -> pd.DataFrame:
    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_csv(DATA_FILE)
            # Normalize columns in case of edits
            for col in ["date", "mood", "note", "score"]:
                if col not in df.columns:
                    df[col] = ""
            return df
        except Exception:
            return pd.DataFrame(columns=["date", "mood", "note", "score"])
    return pd.DataFrame(columns=["date", "mood", "note", "score"])


def save_entry(entry_date: str, mood: str, note: str):
    df = load_log()
    new_row = {
        "date": entry_date,
        "mood": mood,
        "note": note,
        "score": MOOD_SCORE.get(mood, 3),
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)


def normalize_text(t: str) -> str:
    return (t or "").strip().lower()


def detect_risk(text: str) -> str:
    """
    Returns: 'high', 'negative', 'positive', or 'neutral'
    """
    t = normalize_text(text)

    if any(p in t for p in HIGH_DISTRESS_PHRASES):
        return "high"

    neg_hits = sum(1 for w in NEGATIVE_WORDS if w in t)
    pos_hits = sum(1 for w in POSITIVE_WORDS if w in t)

    if neg_hits >= 2 and neg_hits >= pos_hits:
        return "negative"
    if pos_hits >= 2 and pos_hits > neg_hits:
        return "positive"
    if neg_hits >= 1 and neg_hits >= pos_hits:
        return "negative"
    if pos_hits >= 1 and pos_hits > neg_hits:
        return "positive"
    return "neutral"


def safety_block():
    st.markdown("### 🚨 Need Immediate Help? (Singapore)")
    st.markdown(
        """
- **Samaritans of Singapore (SOS)**: **1767** (24/7)
- **Institute of Mental Health (IMH) Mental Health Helpline**: **6389 2222** (24/7)
- **Singapore Association for Mental Health (SAMH)**: **1800 283 7019**
- **Singapore Children’s Society (SCS) – Tinkle Friend**: **1800 274 4788** (for children & youth)

If you feel unsafe right now, please call one of the numbers above or reach out to a trusted adult immediately.
"""
    )


# ---------- UI ----------
st.title("MindEase 🌱")
st.caption("A simple, anonymous wellbeing prototype for journaling, self-care, and support.")

with st.expander("Privacy & Disclaimer (tap to read)", expanded=True):
    st.markdown(
        """
**Privacy & Confidentiality**
- No login required
- Do not enter your full name, NRIC, address, or other personal identifiers
- Entries are stored in a simple local file for the prototype (mood_log.csv)

**Disclaimer**
This app provides general self-care suggestions and is **not** a substitute for professional medical advice.
"""
    )

page = st.sidebar.radio(
    "Navigate",
    ["Journal", "Mood Analyzer", "Mood History", "Self-Care Tools", "Support & Hotlines"],
    index=0
)

# ---------- Journal ----------
if page == "Journal":
    st.header("📝 Mood Journal")

    col1, col2 = st.columns(2)
    with col1:
        entry_date = st.date_input("Date", value=date.today()).isoformat()
    with col2:
        mood = st.selectbox("Select your mood", MOODS, index=MOODS.index("Okay"))

    note = st.text_area(
        "Optional notes",
        placeholder="What happened today? Anything you want to remember or reflect on?"
    )

    if st.button("Save Entry"):
        save_entry(entry_date, mood, note)
        st.success("Saved! You can view it in Mood History.")

    st.markdown("---")
    st.markdown("Tip: Journaling works best when it’s quick and consistent. Even one sentence is enough.")

# ---------- Mood Analyzer ----------
elif page == "Mood Analyzer":
    st.header("🧠 Mood Analyzer")

    st.write("Type how you’re feeling. The app will suggest simple self-care tools.")
    text = st.text_area("Your thoughts", placeholder="e.g., I feel stressed about school...")

    if st.button("Analyze"):
        if not text.strip():
            st.warning("Please type something to analyze.")
        else:
            risk = detect_risk(text)

            if risk == "high":
                st.error("It sounds like you may be going through a really hard moment.")
                st.write("You don’t have to handle this alone. Please consider reaching out for help right now.")
                safety_block()

            elif risk == "negative":
                st.info("It seems like you’re feeling stressed or upset.")
                st.markdown("### Quick tools to try now")
                st.markdown(
                    """
**1) Box Breathing (1 minute)**
- Inhale 4 seconds  
- Hold 4 seconds  
- Exhale 4 seconds  
- Hold 4 seconds  
Repeat 3–4 cycles.

**2) Grounding 5–4–3–2–1**
- 5 things you can see  
- 4 things you can feel  
- 3 things you can hear  
- 2 things you can smell  
- 1 thing you can taste
"""
                )
                st.markdown("**Affirmation:** You are doing your best, and that is enough.")
                st.caption("If you feel unsafe or overwhelmed, use the Support & Hotlines page.")
            elif risk == "positive":
                st.success("You seem to be feeling okay or positive.")
                st.markdown("**Affirmation:** Keep going. Small progress is still progress.")
                st.markdown("**Optional prompt:** What’s one thing that went well today?")
            else:
                st.write("Your mood seems neutral or mixed.")
                st.markdown("**Gentle prompt:** What is one small thing you can do in the next 10 minutes to help yourself?")

# ---------- Mood History ----------
elif page == "Mood History":
    st.header("📈 Mood History")

    df = load_log()
    if df.empty:
        st.info("No entries yet. Go to the Journal page to add your first entry.")
    else:
        # Clean types
        df["score"] = pd.to_numeric(df.get("score", 3), errors="coerce").fillna(3)
        # Attempt to parse dates
        df["date"] = df["date"].astype(str)
        try:
            df["_date"] = pd.to_datetime(df["date"])
        except Exception:
            df["_date"] = pd.NaT

        st.subheader("Your entries")
        show_notes = st.checkbox("Show notes", value=True)
        view_cols = ["date", "mood", "score"] + (["note"] if show_notes else [])
        st.dataframe(df[view_cols].sort_values(by="date", ascending=False), use_container_width=True)

        st.subheader("Mood trend")
        chart_df = df.dropna(subset=["_date"]).sort_values(by="_date")
        if chart_df.empty:
            st.warning("Dates couldn’t be parsed for charting, but your table is saved.")
        else:
            st.line_chart(chart_df.set_index("_date")["score"])

        st.markdown("---")
        if st.button("Clear all saved entries (prototype)"):
            if os.path.exists(DATA_FILE):
                os.remove(DATA_FILE)
            st.success("Cleared. Refresh this page.")

# ---------- Self-Care Tools ----------
elif page == "Self-Care Tools":
    st.header("🧰 Self-Care Tools")

    tool = st.selectbox(
        "Choose a tool",
        ["Breathing Timer", "Grounding 5-4-3-2-1", "Affirmations", "Mini Prompts"]
    )

    if tool == "Breathing Timer":
        st.subheader("Breathing Timer (Box Breathing)")
        st.write("Use this pattern: Inhale 4, Hold 4, Exhale 4, Hold 4.")
        cycles = st.slider("Cycles", 2, 8, 4)
        st.info(f"Do {cycles} cycles. Total time: about {cycles*16} seconds.")

    elif tool == "Grounding 5-4-3-2-1":
        st.subheader("Grounding 5–4–3–2–1")
        st.write("Take a slow breath and fill these in:")
        st.text_input("5 things I can see")
        st.text_input("4 things I can feel")
        st.text_input("3 things I can hear")
        st.text_input("2 things I can smell")
        st.text_input("1 thing I can taste")

    elif tool == "Affirmations":
        st.subheader("Affirmations")
        affirmations = [
            "I can take things one step at a time.",
            "My feelings are valid, and they will pass.",
            "I am allowed to ask for help.",
            "I don’t have to be perfect to be worthy.",
            "I can do hard things."
        ]
        st.write("Tap for one:")
        if st.button("Give me an affirmation"):
            st.success(affirmations[datetime.now().second % len(affirmations)])

    else:
        st.subheader("Mini Prompts")
        st.markdown(
            """
- What’s one thing you can control today?
- What’s one tiny action that would help right now?
- If your friend felt this way, what would you tell them?
- What’s one thing you did well today, even if it’s small?
"""
        )

# ---------- Support & Hotlines ----------
else:
    st.header("🆘 Support & Hotlines")
    safety_block()
    st.markdown("---")
    st.markdown(
        """
If you are in danger or need urgent help, contact emergency services immediately.
"""
    )

