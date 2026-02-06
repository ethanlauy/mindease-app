import streamlit as st

st.set_page_config(page_title="MindEase", layout="centered")

st.title("MindEase 🌱")
st.write("A safe, private space for reflection and self-care.")

st.markdown("""
🔒 Privacy & Confidentiality
- Anonymous usage
- No personal data stored
- Not a substitute for professional medical advice
""")

st.markdown("### Daily Mood Journal")

journal = st.text_area(
    "How are you feeling today?",
    placeholder="Type your thoughts here..."
)

if st.button("Analyze Mood"):
    if journal.strip() == "":
        st.warning("Please write something.")
    else:
        text = journal.lower()

        if "sad" in text or "stress" in text or "anxious" in text:
            st.write("You may be feeling stressed.")
            st.write("Try breathing exercise:")
            st.write("Inhale 4 sec, hold 4 sec, exhale 6 sec.")
        else:
            st.write("You seem okay today.")
            st.write("Affirmation: You are doing your best.")

st.markdown("---")
st.markdown("### Need Immediate Help?")

st.markdown("""
SOS Hotline: 1767  
SAMH Hotline: 1800 283 7019  
IMH Hotline: 6389 2222
""")

st.caption("This app does not replace professional medical advice.")
