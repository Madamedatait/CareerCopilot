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
from backend.services.job_tags import build_tags

from backend.config.career_paths import (
    CAREER_PATHS
)

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
                s.name AS source,
                j.location,
                j.job_url,
                j.description
            FROM jobs j
            LEFT JOIN companies c
                ON c.id = j.company_id
            LEFT JOIN sources s
                ON s.id = j.source_id
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

    # -----------------------------------
    # Tags
    # -----------------------------------

    df["Tags"] = df.apply(
        lambda row: build_tags(
            row["Location"],
            row["Description"]
        ),
        axis=1
    )

    # -----------------------------------
    # Source Filter
    # -----------------------------------

    sources = st.multiselect(
        "📦 Sources",
        options=sorted(df["Source"].dropna().unique()),
        default=sorted(df["Source"].dropna().unique())
    )

    df = df[df["Source"].isin(sources)]

    career_paths = st.multiselect(
        "🎯 Career Path",
        options=list(
            CAREER_PATHS.keys()
        ),
        default=[
            "Support",
            "Data"
        ]
    )

    if career_paths:

        mask = False

        search_text = (
            df["Title"].fillna("")
            + " "
            + df["Description"].fillna("")
        )

    for path in career_paths:

        for keyword in CAREER_PATHS[path]:

            mask = mask | search_text.str.contains(
                keyword,
                case=False,
                na=False
            )

        df = df[mask]

    # -----------------------------------
    # Remote Filter
    # -----------------------------------

    remote_only = st.checkbox(
        "🌍 Remote only"
    )

    if remote_only:

        df = df[
            df["Location"].str.contains(
                "remote",
                case=False,
                na=False
            )
        ]

    # -----------------------------------
    # Europe Filter
    # -----------------------------------

    europe_only = st.checkbox(
        "🇪🇺 Europe only"
    )

    if europe_only:

        EUROPE_KEYWORDS = [
            "europe",
            "france",
            "belgium",
            "romania",
            "germany",
            "spain",
            "italy",
            "portugal",
            "netherlands",
            "poland",
            "emea"
        ]

        mask = False

        for keyword in EUROPE_KEYWORDS:

            mask = mask | df["Location"].str.contains(
                keyword,
                case=False,
                na=False
            )

        df = df[mask]
    
    #
    #French Filter
    #

    french_only = st.checkbox("🇫🇷 French")

    if french_only:
        df = df[
            df["Description"].str.contains(
                "french|français",
                case=False,
                na=False,
                regex=True
            )
        ]
    

    #
    #Roumania Filter
    #
    
    romania_only = st.checkbox("🇷🇴 Romania")

    if romania_only:
        df = df[
            df["Description"].str.contains(
                "romania|romanian",
                case=False,
                na=False,
                regex=True
            )
        ]
    
    # -----------------------------------
    # Score Filter
    # -----------------------------------

    minimum_score = st.slider(
        "⭐ Minimum score",
        min_value=0,
        max_value=200,
        value=50
    )

    df = df[
        df["Score"] >= minimum_score
    ]

    # -----------------------------------
    # Search
    # -----------------------------------

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
    # Sort
    # -----------------------------------

    df = df.sort_values(
        by="Score",
        ascending=False
    )

    # -----------------------------------
    # Metrics
    # -----------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Jobs",
            len(df)
        )

    with col2:
        st.metric(
            "Companies",
            df["Company"].nunique()
        )

    with col3:
        st.metric(
            "Sources",
            df["Source"].nunique()
        )

    # -----------------------------------
    # Display DataFrame
    # -----------------------------------

    display_df = df[
        [
            "Score",
            "Title",
            "Company",
            "Source",
            "Tags",
            "Location",
            "URL"
        ]
    ]

    # -----------------------------------
    # Table
    # -----------------------------------

    st.data_editor(
        display_df,
        use_container_width=True,
        disabled=True,
        column_config={
            "URL": st.column_config.LinkColumn(
                "Job Link",
                display_text="Open Job"
            )
        }
    )

except Exception as e:

    st.error(str(e))
