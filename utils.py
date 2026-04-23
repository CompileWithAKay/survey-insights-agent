import pandas as pd

# -------------------------
# LOAD DATA
# -------------------------
def load_data(uploaded_file):
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    return df


# -------------------------
# CLEAN + STRUCTURE DATA
# -------------------------
def clean_data(df):

    # Rename key columns
    df = df.rename(columns={
        "Please tell us which Business Unit you work at": "Business Unit",
        "Please tell us the Function Department you are part of": "Function Department"
    })

    # Map survey responses to numeric
    mapping = {
        "Fully agree": 5,
        "Partially agree": 4,
        "It is hardly the case": 2,
        "I don't agree at all": 1
    }

    df = df.replace(mapping)

    # Columns to exclude from numeric scoring
    exclude_cols = [
        "formName", "dateUTC", "Business Unit", "Function Department",
        "Please indicate which employment status applies to You",
        "Please indicate your position EE level",
        "Employee Group", "Organizational Unit", "Company",
        "Personnel Sub Area", "Position.1"
    ]

    # TEXT / OPEN-ENDED RESPONSES (VERY IMPORTANT)
    text_cols = [
        "If there was one thing about our culture you could improve what would it be",
        "If there was one thing about our culture you believe we need to stop what would it be",
        "In shaping Exxaros aspirational culture how should our culture look and feel in the future",
        "What leadership behaviours and ways of working are most important to make this aspirational culture a reality",
        "What one or two actions would have the biggest positive impact in helping Exxaro achieve this aspirational culture"
    ]

    # Identify survey scoring columns
    survey_cols = [
        col for col in df.columns
        if col not in exclude_cols + text_cols
    ]

    # Convert to numeric
    df[survey_cols] = df[survey_cols].apply(pd.to_numeric, errors='coerce')

    numeric_cols = df[survey_cols].select_dtypes(include='number').columns

    return df, numeric_cols, text_cols


# -------------------------
# THEMES (CORE INSIGHT ENGINE)
# -------------------------
def get_themes():
    return {
        "Leadership": [
            "There is a good level of trust between top management executive team EXCO and employees",
            "I have confidence in the Exxaro top management",
            "The appointment of the new CEO has strengthened my confidence in Exxaros future"
        ],
        "Culture & Safety": [
            "In my department it is safe to speak up about issues",
            "When I disagree with something in my department I am not afraid to challenge it",
            "At work I am encouraged to share my ideas without fear of victimization even if they are different from others"
        ],
        "Engagement": [
            "I am proud to work for Exxaro",
            "If given another opportunity I would still choose Exxaro as my employer of choice"
        ],
        "Growth": [
            "I am frequently sent for training which contributes to my growth and development",
            "I have personally received mentorship andor coaching in my department"
        ],
        "Communication": [
            "There is good communication of what is happening across Exxaro",
            "There is good communication on what is happening at my Business Unit"
        ]
    }


# -------------------------
# THEME SCORING
# -------------------------
def calculate_theme_scores(df, themes):
    theme_scores = {}

    for theme, cols in themes.items():
        valid_cols = [col for col in cols if col in df.columns]

        if valid_cols:
            theme_scores[theme] = df[valid_cols].mean().mean()

    return theme_scores


# -------------------------
# SENTIMENT LABELING
# -------------------------
def label_sentiment(score):
    if score < 3:
        return "Negative"
    elif score < 4:
        return "Neutral"
    else:
        return "Positive"


# -------------------------
# CAMPAIGN RECOMMENDATIONS
# -------------------------
def campaign_recommendation(score):
    if score < 3:
        return "Fix Leadership & Trust Campaign"
    elif score < 4:
        return "Engagement Boost Campaign"
    else:
        return "Advocacy & Branding Campaign"