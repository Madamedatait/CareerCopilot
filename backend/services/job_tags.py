def build_tags(location, description):

    tags = []

    location = str(location).lower()
    description = str(description).lower()

    if "remote" in location:
        tags.append("🌍 Remote")

    if "europe" in location:
        tags.append("🇪🇺 Europe")

    if "emea" in description:
        tags.append("🇪🇺 EMEA")

    if "french" in description:
        tags.append("🇫🇷 French")

    if "français" in description:
        tags.append("🇫🇷 French")

    if "romania" in description:
        tags.append("🇷🇴 Romania")

    if "romanian" in description:
        tags.append("🇷🇴 Romanian")

    return " | ".join(tags)