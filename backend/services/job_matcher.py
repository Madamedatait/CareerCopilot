def calculate_match(cv_text, title, description):

    cv_text = str(cv_text).lower()

    job_text = (
        str(title) + " " + str(description)
    ).lower()

    keywords = {
        "support engineer": 10,
        "technical support": 10,
        "application support": 9,
        "customer support": 9,
        "customer success": 8,

        "incident management": 7,
        "troubleshooting": 7,

        "jira": 5,
        "zendesk": 5,
        "salesforce": 5,

        "python": 4,
        "sql": 4,
        "excel": 3,
        "power bi": 3,
        "tableau": 3,

        "saas": 3,
        "crm": 3,

        "french": 3,
        "romanian": 3,
        "english": 2,

        "analytics": 2,
        "data": 1
    }

    score = 0
    max_score = sum(keywords.values())

    for keyword, weight in keywords.items():

        if keyword in cv_text and keyword in job_text:
            score += weight

    return round(
        score / max_score * 100,
        1
    )