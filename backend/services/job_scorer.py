def calculate_score(
    title,
    description,
    location
):

    title = str(title).lower()
    description = str(description).lower()
    location = str(location).lower()

    score = 0

    # ------------------
    # Support
    # ------------------

    if "platform support engineer" in title:
        score += 100

    elif "technical support engineer" in title:
        score += 95

    elif "application support engineer" in title:
        score += 90

    elif "customer support engineer" in title:
        score += 90

    elif "support engineer" in title:
        score += 85

    # ------------------
    # Data
    # ------------------

    elif "data analyst" in title:
        score += 90

    elif "business analyst" in title:
        score += 85

    elif "data scientist" in title:
        score += 80

    elif "data engineer" in title:
        score += 75

    # ------------------
    # Language bonuses
    # ------------------

    if "french" in description:
        score += 30

    if "français" in description:
        score += 30

    if "romania" in description:
        score += 40

    if "romanian" in description:
        score += 40

    # ------------------
    # Location bonuses
    # ------------------

    if "remote" in location:
        score += 15

    if "europe" in location:
        score += 25

    if "emea" in description:
        score += 20

    # ------------------
    # Generic keywords
    # ------------------

    if "support" in title:
        score += 10

    if "data" in title:
        score += 10

    if "analyst" in title:
        score += 10

    return score