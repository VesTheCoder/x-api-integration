import re


def get_post_ids_from_urls(urls_or_ids: str) -> str:
    """
    Extract tweet IDs from URLs or return clean IDs from input.
    """
    if not urls_or_ids:
        return ""

    items = [item.strip() for item in urls_or_ids.split(",")]
    ids = []

    for item in items:
        if not item:
            continue
        if item.isdigit():
            ids.append(item)
        else:
            match = re.search(r"/status/(\d+)", item)
            if match:
                ids.append(match.group(1))

    return ",".join(ids)
