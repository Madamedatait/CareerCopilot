def calculate_score(title: str):

    title = title.lower()

    score = 0

    if "platform support engineer" in title:
        score += 100

    if "technical support engineer" in title:
        score += 95

    if "application support engineer" in title:
        score += 90

    if "data analyst" in title:
        score += 90

    if "business analyst" in title:
        score += 85

    if "data scientist" in title:
        score += 80

    if "data engineer" in title:
        score += 75

    return score