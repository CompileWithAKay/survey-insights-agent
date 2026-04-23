import streamlit as st
from utils import load_data, clean_data, get_themes, calculate_theme_scores
from ai import generate_summary


st.set_page_config(page_title="Overview", layout="wide")
st.markdown("""
# Autonomous Survey Insights Agent 
### Understand engagement. Identify risks. Drive action.
""")

uploaded_file = st.file_uploader("Upload Survey File", type=["xlsx", "csv"])

if uploaded_file:
    df = load_data(uploaded_file)
    df, numeric_cols, text_cols = clean_data(df)

    st.session_state["df"] = df
    st.session_state["numeric_cols"] = numeric_cols
    st.session_state["text_cols"] = text_cols

    st.success("Data uploaded successfully!")

if "df" in st.session_state:

    df = st.session_state["df"]
    numeric_cols = st.session_state["numeric_cols"]

    st.subheader("📄 Data Preview")
    st.dataframe(df.head())

    # -------------------------
    # OVERALL SCORE
    # -------------------------
    overall_score = df[numeric_cols].mean().mean()
    st.metric("Overall Engagement Score", round(overall_score, 2))

    st.caption(
        "This score represents the average employee sentiment across all survey questions. "
        "It reflects overall engagement, trust, communication, and workplace experience."
    )

    # -------------------------
    # THEME SCORES
    # -------------------------
    themes = get_themes()
    theme_scores = calculate_theme_scores(df, themes)

    st.subheader("📊 Theme Scores")

    cols = st.columns(len(theme_scores))
    for i, (theme, score) in enumerate(theme_scores.items()):
        cols[i].metric(theme, round(score, 2))

    # -------------------------
    # AI SUMMARY
    # -------------------------
    st.subheader("AI Theme Insights")

    if st.button("Generate Theme Insights"):
        with st.spinner("Analyzing themes..."):
            summary = generate_summary(theme_scores, df[numeric_cols].mean())

        st.write(summary)

else:
    st.info("Upload a file to begin.")

st.divider()
st.subheader("💬 Ask Your Data")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_query = st.text_input("Ask a question about the survey data")

if user_query and "df" in st.session_state:

    df = st.session_state["df"]
    numeric_cols = st.session_state["numeric_cols"]

    # Basic context for now (we'll improve later)
    context = {
        "overall_score": float(df[numeric_cols].mean().mean()),
        "sample_data": df.head(5).to_dict()
    }

    prompt = f"""
You are an HR analytics assistant.

User Question:
{user_query}

Dataset Context:
{context}

Rules:
- Only use provided data
- Give concise, insightful answers
- Suggest actions where relevant
"""

    response = generate_summary({"query": prompt}, {})  # reuse Bedrock

    st.session_state.chat_history.append(("user", user_query))
    st.session_state.chat_history.append(("ai", response))

# Display chat history
for role, msg in st.session_state.chat_history:
    if role == "user":
        st.markdown(f"🧑‍💬 **You:** {msg}")
    else:
        st.markdown(f"🤖 **AI:** {msg}")

st.divider()

with st.expander("ℹ️ How Engagement Scores Are Calculated"):
    st.markdown("""
### 📊 Response Conversion Methodology

Survey responses are converted into numerical values to allow quantitative analysis.

| Response Option | Score |
|----------------|------|
| Fully agree | 5 |
| Partially agree | 4 |
| It is hardly the case | 2 |
| I don't agree at all | 1 |

---

### 🧠 How Scores Are Used

- Each survey question is converted into a numeric score (1–5 scale)
- Department / Business Unit scores are calculated by averaging:
  - All responses per question
  - Then averaging across all questions
- Theme scores group related questions (e.g. Leadership, Engagement) and average them

---

### ⚠️ Important Notes

- Higher scores = more positive employee sentiment
- Scores are comparative, not absolute performance ratings
- Missing or invalid responses are excluded from calculations
""")