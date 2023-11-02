def ensure_url_scheme(url):
    """
    Ensure that the URL has a scheme.
    """
    if not url.startswith(("http://", "https://")):
        return "https://" + url
    return url
