# Craftacoder

A wrapper around Aider that provides custom routing capabilities for LLM API calls.

## Installation

### Using Virtual Environment (Recommended)

1. **Create a virtual environment**:
   ```bash
   python -m venv craftacoder-env
   ```

2. **Activate the virtual environment**:
   - On Windows:
     ```bash
     craftacoder-env\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source craftacoder-env/bin/activate
     ```

3. **Install `craftacoder`**:
   ```bash
   pip install craftacoder
   ```

### Without Virtual Environment

1. **Install `craftacoder` directly**:
   ```bash
   pip install craftacoder
   ```

```bash
pip install craftacoder
```

## Usage

To use Craftacoder, you need to acquire an API key from [coder.craftapit.com](https://coder.craftapit.com).

### Acquiring an API Key

1. **Visit the website**:
   - Go to [coder.craftapit.com](https://coder.craftapit.com).
   
2. **Sign Up or Log In**:
   - Create an account or log in if you already have one.
   
3. **Navigate to API Keys Section**:
   - Once logged in, navigate to the section where you can manage your API keys.
   
4. **Generate a New API Key**:
   - Generate a new API key and note it down.

### Running Craftacoder

You can run Craftacoder using command-line arguments or environment variables.

#### Using Command-Line Arguments

```bash
craftacoder --router-url https://coder.craftapit.com --router-api-key your-api-key [aider arguments]
```

#### Using Environment Variables

```bash
export CRAFTACODER_ROUTER_URL=https://coder.craftapit.com
export CRAFTACODER_ROUTER_API_KEY=your-api-key

craftacoder [aider arguments]
```

For PowerShell users:

```powershell
# Set environment variables
$env:CRAFTACODER_ROUTER_URL = "https://coder.craftapit.com"
$env:CRAFTACODER_ROUTER_API_KEY = "your-api-key"

# Run craftacoder
craftacoder [aider arguments]

# Or use directly with arguments
craftacoder --router-url https://coder.craftapit.com --router-api-key your-api-key [aider arguments]
```

## Features

- Custom routing of LLM API calls
- Centralized API key management
- Support for multiple LLM providers
- Compatible with all Aider features
