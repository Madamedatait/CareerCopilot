import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
from pathlib import Path
import sys

# -----------------------------------
# Import backend
# -----------------------------------

ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))

from backend.services.job_scorer import calculate_score

# -----------------------------------
# Configuration
# -----------------------------------

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

# -----------------------------------
# UI
# -----------------------------------

st.set_page_config(
    page_title="CareerCopilot",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 CareerCopilot")

try:

    # -----------------------------------
    # Load jobs
    # -----------------------------------

    with engine.connect() as conn:

        result = conn.execute(text("""
            SELECT
                j.title,
                c.name,
                s.name as source,
                j.location,
                j.job_url,
                j.description
            FROM jobs j
            LEFT JOIN companies c
                ON c.id = j.company_id
        """))

        rows = result.fetchall()

    # -----------------------------------
    # DataFrame
    # -----------------------------------

    df = pd.DataFrame(
        rows,
        columns=[
            "Title",
            "Company",
            "Source",
            "Location",
            "URL",
            "Description"
        ]
    )

    # -----------------------------------
    # Score
    # -----------------------------------

    df["Score"] = df.apply(
    lambda row: calculate_score(
        row["Title"],
        row["Description"],
        row["Location"]
    ),
    axis=1
)

    df = df.sort_values(
        by="Score",
        ascending=False
    )

    # -----------------------------------
    # Filters
    # -----------------------------------

    minimum_score = st.slider(
        "⭐ Minimum score",
        min_value=0,
        max_value=100,
        value=50
    )

    df = df[df["Score"] >= minimum_score]

    search = st.text_input(
        "🔎 Search jobs"
    )

    if search:

        df = df[
            df["Title"].str.contains(
                search,
                case=False,
                na=False
            )
            |
            df["Company"].str.contains(
                search,
                case=False,
                na=False
            )
        ]

    # -----------------------------------
    # Display
    # -----------------------------------

    df = df[
        [
            "Score",
            "Title",
            "Company",
            "Location",
            "URL"
        ]
    ]

    st.metric(
        "Jobs found",
        len(df)
    )

    st.data_editor(
    df,
    use_container_width=True,
    disabled=True,
    column_config={
        "URL": st.column_config.LinkColumn(
            "URL"
        )
    }
)

except Exception as e:

    st.error(str(e))