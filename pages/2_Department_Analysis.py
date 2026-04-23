import streamlit as st
from utils import get_themes

st.title("Department Analysis")

if "df" not in st.session_state:
    st.warning("Upload data in Overview first.")
    st.stop()

df = st.session_state["df"]
numeric_cols = st.session_state["numeric_cols"]

themes = get_themes()

# -------------------------
# FILTER
# -------------------------
selected_dept = st.selectbox(
    "Select Department",
    sorted(df["Function Department"].dropna().unique())
)

filtered_df = df[df["Function Department"] == selected_dept]

# -------------------------
# THEME SCORES
# -------------------------
theme_scores = {
    theme: filtered_df[cols].mean().mean()
    for theme, cols in themes.items()
    if all(col in filtered_df.columns for col in cols)
}

st.subheader(f"Theme Breakdown - {selected_dept.title()}")
st.bar_chart(theme_scores)

# -------------------------
# DRIVER ANALYSIS
# -------------------------
st.subheader("Key Drivers")

st.caption(
    "Key drivers highlight the survey questions that most influence engagement. "
    "Low scores indicate problem areas, while high scores show strengths."
)

question_scores = filtered_df[numeric_cols].mean().sort_values()

weak = question_scores.head(3)
strong = question_scores.tail(3)

st.write("🔴 Weakest Areas")
for q, score in weak.items():
    st.write(f"- {q} → {round(score,2)} (Needs attention)")

st.write("🟢 Strongest Areas")
for q, score in strong.items():
    st.write(f"- {q} → {round(score,2)} (Strong performance)")