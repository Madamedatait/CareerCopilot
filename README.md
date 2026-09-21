# 🚀 CareerCopilot

CareerCopilot is a job search application designed to help candidates find and filter remote and European job opportunities based on their profile, skills and career goals.

The application collects job offers from multiple sources, stores them in a PostgreSQL database and provides a Streamlit interface for searching, filtering and matching opportunities.

---

## ✨ Features

### 🔍 Job Board

Browse job opportunities collected from multiple job platforms and company job boards.

Available filters include:

- 🎯 Career Path
- 🌍 Remote jobs
- 🇪🇺 Europe
- 🇫🇷 French
- 🇷🇴 Romania
- ⭐ Minimum score
- 🔎 Job title or company search

---

### 📄 CV Matcher

Upload a PDF CV and compare it with available job opportunities.

CareerCopilot:

1. Extracts the text from the CV
2. Analyzes job titles and descriptions
3. Detects matching skills and keywords
4. Calculates a match percentage
5. Displays the best matching opportunities

---

## 📊 Job Scoring

CareerCopilot assigns a score to job opportunities based on several criteria, including:

- Support engineering roles
- Data and analytics roles
- French language
- Romanian language
- Remote opportunities
- European locations
- Relevant keywords

The scoring system is implemented in Python and can be extended as the project evolves.

---

## 🏗️ Architecture

```text
Job Sources
     │
     ▼
Collectors
     │
     ▼
Job Filtering / Normalization
     │
     ▼
PostgreSQL / Supabase
     │
     ▼
Python Services
     │
     ├── Job Scoring
     ├── Job Tags
     └── CV Matching
     │
     ▼
Streamlit Application