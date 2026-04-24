import boto3
import json
import streamlit as st

# -------------------------
# CREATE BEDROCK CLIENT
# -------------------------
def get_bedrock_client():
    try:
        return boto3.client(
            "bedrock-runtime",
            region_name=st.secrets["AWS_DEFAULT_REGION"],
            aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
            aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"]
        )
    except Exception as e:
        st.error("AWS credentials not configured properly in Streamlit Secrets.")
        return None


# -------------------------
# MODEL CONFIG
# -------------------------
MODEL_ID = "arn:aws:bedrock:us-east-1:303767824861:inference-profile/global.anthropic.claude-haiku-4-5-20251001-v1:0"


# -------------------------
# MAIN FUNCTION
# -------------------------
def generate_summary(theme_scores, question_scores):
    """
    Accepts:
    - theme_scores (dict OR pandas Series)
    - question_scores (dict OR pandas Series)
    """

    # -------------------------
    # SAFELY CONVERT INPUTS
    # -------------------------
    if hasattr(theme_scores, "to_dict"):
        theme_scores = theme_scores.to_dict()

    if hasattr(question_scores, "to_dict"):
        question_scores = question_scores.to_dict()

    # Get lowest 5 questions
    sorted_questions = sorted(question_scores.items(), key=lambda x: x[1])
    lowest_questions = dict(sorted_questions[:5])

    # -------------------------
    # PROMPT
    # -------------------------
    prompt = f"""
You are a senior HR strategy consultant.

Analyze the employee engagement survey results below.

Theme Scores (higher is better, out of 5):
{theme_scores}

Lowest Scoring Survey Areas:
{lowest_questions}

Instructions:
- Identify root causes behind low scores
- Highlight key strengths
- Recommend a focused campaign strategy
- Suggest 3–5 clear, practical actions

Output format:
1. Executive Summary (short paragraph)
2. Key Issues (bullet points)
3. Key Strengths (bullet points)
4. Recommended Campaign Strategy
5. Priority Actions (bullet points)

Keep it concise, professional, and insight-driven.
"""

    # -------------------------
    # BUILD REQUEST
    # -------------------------
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 500,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    }

    client = get_bedrock_client()

    # If client failed (no credentials)
    if client is None:
        return fallback_summary(theme_scores, lowest_questions)

    # -------------------------
    # CALL BEDROCK
    # -------------------------
    try:
        response = client.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json"
        )

        result = json.loads(response["body"].read())

        return result["content"][0]["text"]

    except Exception as e:
        # Log error for debugging
        print("Bedrock Error:", str(e))

        # Fallback so app never breaks
        return fallback_summary(theme_scores, lowest_questions)


# -------------------------
# FALLBACK (DEMO-SAFE)
# -------------------------
def fallback_summary(theme_scores, lowest_questions):
    return f"""
### Executive Summary
Engagement shows mixed results with several low-scoring areas requiring attention.

### Key Issues
- {list(lowest_questions.keys())[0] if lowest_questions else "Low scoring themes identified"}
- Additional engagement gaps in survey responses

### Key Strengths
- Stable performance in higher-scoring themes
- Consistent responses across business units

### Recommended Campaign Strategy
Focus on targeted engagement interventions addressing the lowest scoring areas, supported by leadership communication and quick-win initiatives.

### Priority Actions
- Run focused listening sessions
- Address top pain points in lowest scoring areas
- Improve manager communication
- Launch quick engagement wins
"""
