import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
from pathlib import Path
import sys

from backend.config.career_paths import (
    CAREER_PATHS
)

# -----------------------------------
# Import backend
# -----------------------------------

ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))

from backend.services.cv_parser import extract_text_from_pdf
from backend.services.job_matcher import calculate_match

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
    page_title="CV Matcher",
    page_icon="📄",
    layout="wide"
)

st.title("📄 CV Matcher")

uploaded_file = st.file_uploader(
    "Upload your CV",
    type=["pdf"]
)

if uploaded_file:

    # -----------------------------------
    # Extract CV text
    # -----------------------------------

    cv_text = extract_text_from_pdf(
        uploaded_file
    )

    st.success(
        "CV uploaded successfully"
    )

    # -----------------------------------
    # Preview
    # -----------------------------------

    with st.expander("📖 CV Preview"):

        st.text_area(
            "Extracted text",
            cv_text[:3000],
            height=300
        )

    # -----------------------------------
    # Load Jobs
    # -----------------------------------

    with engine.connect() as conn:

        result = conn.execute(text("""
            SELECT
                j.title,
                c.name,
                s.name as source,
                j.location,
                j.description,
                j.job_url
            FROM jobs j
            LEFT JOIN companies c
                ON c.id = j.company_id
            LEFT JOIN sources s
                ON s.id = j.source_id
        """))

        rows = result.fetchall()

    jobs_df = pd.DataFrame(
        rows,
        columns=[
            "Title",
            "Company",
            "Source",
            "Location",
            "Description",
            "URL"
        ]
    )

    # -----------------------------------
    # Matching
    # -----------------------------------

    jobs_df["Match"] = jobs_df.apply(
        lambda row: calculate_match(
            cv_text,
            row["Title"],
            row["Description"]
        ),
        axis=1
    )

    # -----------------------------------
    # Filters
    # -----------------------------------

    sources = st.multiselect(
        "📦 Sources",
        options=sorted(
            jobs_df["Source"].dropna().unique()
        ),
        default=sorted(
            jobs_df["Source"].dropna().unique()
        )
    )

    jobs_df = jobs_df[
        jobs_df["Source"].isin(sources)
    ]

    remote_only = st.checkbox(
        "🌍 Remote only"
    )

    if remote_only:

        jobs_df = jobs_df[
            jobs_df["Location"].str.contains(
                "remote",
                case=False,
                na=False
            )
        ]

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

            mask = mask | jobs_df[
                "Location"
            ].str.contains(
                keyword,
                case=False,
                na=False
            )

        jobs_df = jobs_df[mask]

    minimum_match = st.slider(
        "🎯 Minimum Match",
        min_value=0,
        max_value=100,
        value=10
    )

    jobs_df = jobs_df[
        jobs_df["Match"] >= minimum_match
    ]

    search = st.text_input(
        "🔎 Search"
    )

    if search:

        jobs_df = jobs_df[
            jobs_df["Title"].str.contains(
                search,
                case=False,
                na=False
            )
            |
            jobs_df["Company"].str.contains(
                search,
                case=False,
                na=False
            )
        ]


    career_paths = st.multiselect(
        "🎯 Career Path",
        options=list(CAREER_PATHS.keys()),
        default=[
            "Support",
            "Data"
        ]
    )

    search_text = (
        jobs_df["Title"].fillna("")
        + " "
        + jobs_df["Description"].fillna("")
    )

    if career_paths:

        mask = False

        for path in career_paths:

            for keyword in CAREER_PATHS[path]:

                mask = mask | search_text.str.contains(
                    keyword,
                    case=False,
                    na=False
                )

        jobs_df = jobs_df[mask]

    french_only = st.checkbox(
        "🇫🇷 French"
    )

    if french_only:

        jobs_df = jobs_df[
            jobs_df["Description"].str.contains(
                "french|français",
                case=False,
                na=False,
                regex=True
            )
        ]

    romania_only = st.checkbox(
        "🇷🇴 Romania"
    )

    if romania_only:

        jobs_df = jobs_df[
            jobs_df["Description"].str.contains(
                "romania|romanian",
                case=False,
                na=False,
                regex=True
            )
        ]
    
    # -----------------------------------
    # Sort
    # -----------------------------------

    jobs_df = jobs_df.sort_values(
        by="Match",
        ascending=False
    )

    top_jobs = jobs_df.head(20)

    # -----------------------------------
    # Metrics
    # -----------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Jobs",
            len(jobs_df)
        )

    with col2:

        best_match = (
            top_jobs["Match"].max()
            if not top_jobs.empty
            else 0
        )

        st.metric(
            "Best Match",
            f"{best_match}%"
        )

    with col3:
        st.metric(
            "Sources",
            jobs_df["Source"].nunique()
        )

    # -----------------------------------
    # Results
    # -----------------------------------

    st.subheader(
        "🎯 Top 20 Matches"
    )

    st.data_editor(
        top_jobs[
            [
                "Match",
                "Title",
                "Company",
                "Source",
                "Location",
                "URL"
            ]
        ],
        width="stretch",
        disabled=True,
        column_config={
            "URL": st.column_config.LinkColumn(
                "Job Link",
                display_text="Open Job"
            )
        }
    )