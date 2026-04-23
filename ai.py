import boto3
import json

# Bedrock runtime client
client = boto3.client("bedrock-runtime", region_name="us-east-1")

# Model ID
MODEL_ID = "arn:aws:bedrock:us-east-1:303767824861:inference-profile/global.anthropic.claude-haiku-4-5-20251001-v1:0"


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
    # IMPROVED PROMPT
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
    # BEDROCK REQUEST
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

    response = client.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )

    result = json.loads(response["body"].read())

    # -------------------------
    # SAFE RESPONSE PARSING
    # -------------------------
    try:
        return result["content"][0]["text"]
    except (KeyError, IndexError):
        return str(result)