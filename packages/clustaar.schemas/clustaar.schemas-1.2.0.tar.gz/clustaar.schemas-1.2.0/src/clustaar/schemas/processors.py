import bleach
import unicodedata

SANE_TAGS = bleach.sanitizer.ALLOWED_TAGS + ["br"]
ALLOWED_ATTRIBUTES = bleach.sanitizer.ALLOWED_ATTRIBUTES.copy()


def a_filter(tag: str, attr: str, value: str) -> bool:
    """
    filter for <a> html tag.
    Allow "href" and "title" and "target" for some values
    Args:
        tag: html tag : always <a> since used in "a" key of ALLOWED_ATTRIBUTE
        attr: tag attribute
        value: attribute value

    Returns:
        True if keep the attribute
    """
    if attr in ["href", "title"]:
        return True
    if attr == "target" and value in ["_blank", "_top"]:
        return True
    return False


ALLOWED_ATTRIBUTES["a"] = a_filter


def html_sanitize(value):
    """
    Sanitize HTML in value to avoid malicious usage.
    Bleach is a bit excessive with the ampersands, and we prefer to keep it as they were.
    """
    return (
        bleach.clean(value, tags=SANE_TAGS, attributes=ALLOWED_ATTRIBUTES).replace("&amp;", "&")
        if value
        else value
    )


def unicode_normalize(value):
    """Normalize input to ensure clean encoding in db"""
    return unicodedata.normalize("NFKC", value) if value else value
