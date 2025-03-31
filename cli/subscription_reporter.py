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
    Get token information from the router API.
    Returns a tuple of (used_tokens, total_tokens, percentage, is_unlimited)
    """
    try:
        if not router_url or not router_api_key:
            logger.debug("Router URL or key not provided")
            return None, None, None, False

        # Construct the token usage endpoint from the router URL
        token_usage_endpoint = f"{router_url}/usage"
        
        logger.debug(f"Fetching token info from {token_usage_endpoint}")
        response = requests.get(
            token_usage_endpoint,
            headers={"Authorization": f"Bearer {router_api_key}"},
            timeout=5
        )

        if response.status_code == 200:
            data = response.json()
            used_tokens = data.get("used_tokens", 0)
            total_tokens = data.get("total_tokens", 0)
            is_unlimited = data.get("is_unlimited", False) or total_tokens == 0

            # Calculate percentage
            if is_unlimited:
                percentage = 0
            elif total_tokens > 0:
                percentage = (used_tokens / total_tokens) * 100
            else:
                percentage = 0

            logger.debug(f"Token info: used={used_tokens}, total={total_tokens}, unlimited={is_unlimited}")
            return used_tokens, total_tokens, percentage, is_unlimited
        else:
            logger.warning(f"Failed to fetch token info: HTTP {response.status_code}")
            return None, None, None, False
    except Exception as e:
        logger.exception(f"Error fetching token info: {e}")
        return None, None, None, False

# Create a closure to store the router URL and API key
def create_patched_methods(router_url, router_api_key):
    def patched_calculate_and_show_tokens_and_cost(self, messages, completion=None):
        # Still call the original to maintain internal state
        original_calculate_and_show_tokens_and_cost(self, messages, completion)
        
        used_tokens, total_tokens, percentage, is_unlimited = get_token_info(router_url, router_api_key)

        # Format the custom usage report
        tokens_report = f"Tokens: {format_tokens(self.message_tokens_sent)} sent, {format_tokens(self.message_tokens_received)} received"

        if used_tokens is not None:
            if is_unlimited:
                subscription_report = f"Subscription: {format_tokens(used_tokens)} used of unlimited tokens"
            else:
                subscription_report = f"Subscription: {format_tokens(used_tokens)} used of {format_tokens(total_tokens)} ({percentage:.1f}%)"
        else:
            # API call failed, but we still want to show a custom message
            subscription_report = "Subscription: Token information unavailable"

        # Replace the usage report with our custom one
        self.usage_report = f"{tokens_report}. {subscription_report}."

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
