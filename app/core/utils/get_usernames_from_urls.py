def get_usernames_from_urls(urls_or_usernames: str) -> str:
    """
    Extract usernames from profile URLs or return clean usernames from input.
    """
    if not urls_or_usernames:
        return ""

    items = [item.strip() for item in urls_or_usernames.split(",")]
    usernames = []

    for item in items:
        if not item:
            continue
        if "/" in item:
            parts = [p for p in item.rstrip("/").split("/") if p]
            if parts:
                usernames.append(parts[-1])
        else:
            usernames.append(item)

    return ",".join(usernames)
