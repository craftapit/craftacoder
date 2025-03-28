import os
import sys
import argparse
from .router_config import configure_router
from .utils import validate_router_config, format_router_url


def main():
    print("craftacoder powered by aider!")

    # Create a parser for your custom arguments
    parser = argparse.ArgumentParser(description="craftacoder powered by Aider")

    # Add your custom arguments
    parser.add_argument(
        "--router-url",
        help="Base URL for the router service",
        default=os.environ.get("CRAFTACODER_ROUTER_URL")
    )
    parser.add_argument(
        "--router-api-key",
        help="API key for the router service",
        default=os.environ.get("CRAFTACODER_ROUTER_API_KEY")
    )

    # Parse just your arguments first
    known_args, remaining_args = parser.parse_known_args()

    # Configure the router if needed
    if not validate_router_config(known_args.router_url, known_args.router_api_key):
        print("Error: Both router URL and API key must be provided")
        return 1        

    formatted_url = format_router_url(known_args.router_url)
    configure_router(
        formatted_url,
        known_args.router_api_key
    )
    print(f"Router configured with URL: {formatted_url}")

    from aider.main import main as aider_main
    # Call the original aider main function with the remaining args
    return aider_main(remaining_args)

if __name__ == "__main__":
    sys.exit(main())
