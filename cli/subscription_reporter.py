import os
import sys
import requests
import logging
import aider.coders.base_coder
from aider.utils import format_tokens

# Store the original methods
original_calculate_and_show_tokens_and_cost = aider.coders.base_coder.Coder.calculate_and_show_tokens_and_cost
original_show_usage_report = aider.coders.base_coder.Coder.show_usage_report

logger = logging.getLogger(__name__)

def get_token_info(router_url, router_api_key):
    """
    Get subscription usage information from the router API.
    Returns the depleted percentage of the subscription.
    """
    try:
        if not router_url or not router_api_key:
            logger.debug("Router URL or key not provided")
            return None

        # Construct the token usage endpoint from the router URL
        token_usage_endpoint = f"{router_url}/providers/subscription-stats"
        
        logger.debug(f"Fetching subscription info from {token_usage_endpoint}")
        response = requests.get(
            token_usage_endpoint,
            headers={"craft-api-key": router_api_key},
            timeout=5
        )

        if response.status_code == 200:
            data = response.json()
            depleted_percentage = data.get("depletedPercentage", 0)
            logger.debug(f"Subscription info: depleted={depleted_percentage}%")
            return depleted_percentage
        else:
            logger.warning(f"Failed to fetch subscription info: HTTP {response.status_code}")
            return None
    except Exception as e:
        logger.exception(f"Error fetching subscription info: {e}")
        return None

# Create a closure to store the router URL and API key
def create_patched_methods(router_url, router_api_key):
    def patched_calculate_and_show_tokens_and_cost(self, messages, completion=None):
        # Still call the original to maintain internal state
        original_calculate_and_show_tokens_and_cost(self, messages, completion)
        
        depleted_percentage = get_token_info(router_url, router_api_key)

        # Format the custom usage report
        tokens_report = f"Tokens: {format_tokens(self.message_tokens_sent)} sent, {format_tokens(self.message_tokens_received)} received"

        if depleted_percentage is not None:
            # Create a visual progress bar
            bar_length = 20
            filled_length = int(bar_length * depleted_percentage / 100)
            bar = '█' * filled_length + '░' * (bar_length - filled_length)
            
            subscription_report = f"Subscription: {bar} {depleted_percentage:.1f}% used"
        else:
            # API call failed, but we still want to show a custom message
            subscription_report = "Subscription: usage data unavailable"

        # Replace the usage report with our custom one
        self.usage_report = f"{tokens_report}. {subscription_report}"

    def patched_show_usage_report(self):
        if not self.usage_report:
            return

        self.io.tool_output(self.usage_report)

        # Preserve the original analytics values
        prompt_tokens = self.message_tokens_sent
        completion_tokens = self.message_tokens_received

        # Keep the original cost values for analytics
        original_message_cost = self.message_cost
        original_total_cost = self.total_cost

        self.event(
            "message_send",
            main_model=self.main_model,
            edit_format=self.edit_format,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
            cost=original_message_cost,  # Preserve original cost for analytics
            total_cost=original_total_cost,  # Preserve original total cost for analytics
        )

        self.message_cost = 0.0
        self.message_tokens_sent = 0
        self.message_tokens_received = 0
    
    return patched_calculate_and_show_tokens_and_cost, patched_show_usage_report

def setup_subscription_reporting(router_url, router_api_key):
    """Apply the monkey patches to customize token reporting."""
    logger.debug("Setting up subscription usage reporting")
    
    # Create patched methods with the provided router URL and API key
    patched_calculate, patched_show = create_patched_methods(router_url, router_api_key)
    
    # Apply the patches
    aider.coders.base_coder.Coder.calculate_and_show_tokens_and_cost = patched_calculate
    aider.coders.base_coder.Coder.show_usage_report = patched_show
    
    logger.debug("Subscription usage reporting enabled")
