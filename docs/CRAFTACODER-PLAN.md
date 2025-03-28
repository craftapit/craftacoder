# Overview

This solution creates a wrapper around Aider that configures a custom router for all LLM API calls. The router acts as a
proxy between Aider and LLM providers (OpenAI, Anthropic, etc.), allowing centralized API key management and request
routing.

## Implementation Approach

1. Create a standalone wrapper project that imports and extends Aider
2. Configure LiteLLM providers to use the router before Aider initialization
3. Pass through all standard Aider arguments while adding custom router options

## Project Structure

```
(git root)
├──craftacoder/
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── main.py           # Custom entry point
│   │   ├── router_config.py  # Router configuration
│   │   └── utils.py          # Utility functions
│   └── docs/
│   │   └── PLAN.md           # This document
│   ├── setup.py              # Packaging
│   ├── requirements.txt      # Dependencies
│   └── README.md            # Documentation
```

## Key Components

### Custom Entry Point (main.py)

- Parses router-specific command line arguments
- Configures the router before initializing Aider
- Passes remaining arguments to Aider's main function

### Router Configuration (router_config.py)

- Uses LiteLLM's configure_provider method to set custom API endpoints
- Maps model names to their respective providers
- Sets custom headers for router authentication

### Package Setup (setup.py)

- Defines dependencies including Aider
- Creates a custom command-line entry point

## Command Line Arguments

- --router-url: Base URL for the router service
- --router-api-key: API key for the router service

## Environment Variables

- CRAFTACODER_ROUTER_URL: Router URL
- CRAFTACODER_ROUTER_API_KEY: Router API key

## Security Benefits

- Provider API keys are not sent to the router
- Router authentication uses a separate API key
- No modification of Aider's core codebase
- Clean separation of concerns

## Usage Example

```bash
craftacoder --router-url https://api.coder.craftapit.com --router-api-key actual_api_key file1.py file2.py
```

This approach provides a non-invasive way to extend Aider with custom routing functionality while maintaining
compatibility with future Aider updates.


