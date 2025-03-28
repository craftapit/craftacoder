import os


def get_provider_from_model(model_name):
    """Determine the provider based on model name."""
    model_name = model_name.lower()

    if model_name.startswith("gpt-") or "openai" in model_name:
        return "openai"
    elif "claude" in model_name:
        return "anthropic"
    elif "gemini" in model_name or "palm" in model_name:
        return "google"
    # Add more providers as needed

    # Default to openai if unknown
    return "openai"

def configure_router(router_url, router_api_key):
    """Configure LiteLLM to use the router for all providers."""

    # Set environment variables for litellm with provider-specific endpoints
    os.environ["OPENAI_API_BASE"] = f"{router_url}/providers/openai"
    os.environ["OPENAI_API_KEY"] = router_api_key
    os.environ["ANTHROPIC_API_BASE"] = f"{router_url}/providers/anthropic"
    os.environ["ANTHROPIC_API_KEY"] = router_api_key
    os.environ["GOOGLE_API_BASE"] = f"{router_url}/providers/google"
    os.environ["GOOGLE_API_KEY"] = router_api_key
    os.environ["OLLAMA_API_BASE"] = f"{router_url}/providers/craftapit"
    os.environ["OLLAMA_API_KEY"] = router_api_key
    

    # Set environment variable to indicate router is configured
    os.environ["CRAFTACODER_ROUTER_CONFIGURED"] = "true"

    return True


