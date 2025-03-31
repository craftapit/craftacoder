import os
import sys
import argparse
import logging
from .router_config import configure_router
from .utils import validate_router_config, format_router_url
from .subscription_reporter import setup_subscription_reporting


def main():
    # Set up logging for debugging
    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    
    logger.debug("Starting craftacoder powered by aider!")
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
    logger = logging.getLogger(__name__)
    logger.debug(f"Router URL: {known_args.router_url}, API Key provided: {'Yes' if known_args.router_api_key else 'No'}")
    
    if not validate_router_config(known_args.router_url, known_args.router_api_key):
        print("Error: Both router URL and API key must be provided")
        return 1        

    formatted_url = format_router_url(known_args.router_url)
    logger.debug(f"Formatted URL: {formatted_url}")
    
    configure_router(
        formatted_url,
        known_args.router_api_key
    )
    print(f"Router configured with URL: {formatted_url}")
    
    # Enable subscription usage reporting with the same router URL and API key
    logger.debug("Enabling subscription usage reporting")
    setup_subscription_reporting(formatted_url, known_args.router_api_key)
    print("Subscription usage reporting enabled")

    try:
        from aider.main import main as aider_main
        logger = logging.getLogger(__name__)
        logger.debug(f"Calling aider_main with args: {remaining_args}")
        # Call the original aider main function with the remaining args
        return aider_main(remaining_args)
    except Exception as e:
        logger.exception(f"Error in aider_main: {e}")
        raise

if __name__ == "__main__":
    sys.exit(main())
