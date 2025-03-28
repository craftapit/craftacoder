def validate_router_config(router_url: str, router_api_key: str) -> bool:
    """Validate router configuration parameters."""
    if not router_url:
        return False
    if not router_api_key:
        return False
    return True

def format_router_url(url: str) -> str:
    """Ensure router URL is properly formatted."""
    url = url.strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url.rstrip('/')
