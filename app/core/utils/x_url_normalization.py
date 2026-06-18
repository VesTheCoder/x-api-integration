import re


def normalize_usernames(values: list[str]) -> list[str]:
    """
    Extract usernames from profile URLs or return clean usernames.
    """
    seen: set[str] = set()
    result: list[str] = []
    for item in values:
        clean = item.strip()
        if not clean:
            continue
        if "/" in clean:
            parts = [p for p in clean.rstrip("/").split("/") if p]
            if parts:
                clean = parts[-1]
        if clean and clean not in seen:
            seen.add(clean)
            result.append(clean)
    return result


def normalize_tweet_ids(values: list[str]) -> list[str]:
    """
    Extract tweet IDs from URLs or return clean IDs.
    """
    seen: set[str] = set()
    result: list[str] = []
    for item in values:
        clean = item.strip()
        if not clean:
            continue
        if clean.isdigit():
            pass
        else:
            match = re.search(r"/status/(\d+)", clean)
            if match:
                clean = match.group(1)
            else:
                continue
        if clean and clean not in seen:
            seen.add(clean)
            result.append(clean)
    return result


def normalize_single_tweet_id(value: str) -> str:
    """
    Extract tweet ID from URL or return clean ID.
    """
    clean = value.strip()
    if clean.isdigit():
        return clean
    match = re.search(r"/status/(\d+)", clean)
    if match:
        return match.group(1)
    return clean
