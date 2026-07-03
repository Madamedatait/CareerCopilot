from backend.config.profile import TARGET_KEYWORDS


def is_relevant_job(job):

    position = job.get("position", "").lower()

    tags = " ".join(job.get("tags", [])).lower()

    searchable_text = f"{position} {tags}"

    return any(
        keyword.lower() in searchable_text
        for keyword in TARGET_KEYWORDS
    )