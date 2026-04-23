import streamlit as st
from utils import get_themes
from ai import generate_summary

st.title("🤖 Campaign Strategy Engine")

if "df" not in st.session_state:
    st.warning("Upload data in Overview first.")
    st.stop()

df = st.session_state["df"]
numeric_cols = st.session_state["numeric_cols"]
text_cols = st.session_state["text_cols"]

themes = get_themes()

# -------------------------
# THEME ANALYSIS
# -------------------------
theme_scores = {
    theme: df[cols].mean().mean()
    for theme, cols in themes.items()
    if all(col in df.columns for col in cols)
}

weakest_theme = min(theme_scores, key=theme_scores.get)

st.subheader("Strategic Focus Area")
st.error(f"🔴 Weakest Theme: {weakest_theme}")

# -------------------------
# QUESTION ANALYSIS
# -------------------------
question_scores = df[numeric_cols].mean().sort_values()

st.subheader("Key Problem Areas")
st.dataframe(question_scores.head(5))

# -------------------------
# TEXT INSIGHTS
# -------------------------
st.subheader("Employee Voice")

for col in text_cols[:2]:
    st.write(f"**{col}**")
    st.write(df[col].dropna().head(5))

# -------------------------
# CAMPAIGN RECOMMENDATION
# -------------------------
st.subheader("📢 Recommended Campaign")

if weakest_theme == "Leadership":
    st.write("Focus on rebuilding trust in leadership and transparency.")
elif weakest_theme == "Culture & Safety":
    st.write("Focus on psychological safety and encouraging open communication.")
elif weakest_theme == "Growth":
    st.write("Focus on career development, training, and mentorship.")
elif weakest_theme == "Communication":
    st.write("Improve internal communication clarity and consistency.")
elif weakest_theme == "Engagement":
    st.write("Boost recognition, pride, and employee advocacy.")

# -------------------------
# AI SUMMARY
# -------------------------
st.subheader("AI Executive Summary")

if st.button("Generate AI Summary"):
    with st.spinner("Generating insights..."):
        summary = generate_summary(theme_scores, question_scores)

    st.success("Summary generated!")
    st.write(summary)