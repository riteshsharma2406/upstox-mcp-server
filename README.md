# Upstox MCP Server

A Python-based [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that connects Claude Desktop to the Upstox API, giving AI-assisted access to Indian stock market data and trading account information.

This project demonstrates how to integrate a financial API with an AI assistant using Python, OAuth authentication, and MCP tools.

> **Current scope:** Read-only access to account information and market data. Order placement and trade execution are **not** implemented.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Upstox API Configuration](#upstox-api-configuration)
- [Claude Desktop Integration](#claude-desktop-integration)
- [Example Prompts](#example-prompts)
- [Development and Testing](#development-and-testing)
- [Security Considerations](#security-considerations)
- [Current Limitations](#current-limitations)
- [Roadmap](#roadmap)
- [Disclaimer](#disclaimer)

---

## Features

### Account Information
- Retrieve the authenticated user's profile
- Retrieve funds and margin information
- View long-term holdings
- Retrieve current trading positions
- View the order book

### Market Data
- Search for supported market instruments
- Retrieve market quotes for specified instruments
- Fetch historical candlestick data
- Retrieve intraday candlestick data (once the corresponding tool is implemented and enabled)

### AI Integration
- Connect Upstox API tools to Claude Desktop via MCP
- Retrieve financial data through natural-language prompts
- Support AI-assisted stock research using quotes and historical prices
- Keep API data retrieval separate from AI interpretation and analysis

### Authentication
- OAuth-based Upstox authorization
- Local storage of the access token
- Reauthorization when the access token expires

---

## Tech Stack

| Component            | Technology            |
|----------------------|-----------------------|
| Language             | Python                |
| AI integration       | Model Context Protocol|
| MCP framework        | FastMCP               |
| HTTP client          | HTTPX                 |
| Authentication       | Upstox OAuth          |
| Configuration        | python-dotenv         |
| AI assistant         | Claude Desktop        |
| Market data provider | Upstox API            |

---

## Architecture

```
┌──────────────────────────┐
│      Claude Desktop      │
│  Natural-language prompts│
└────────────┬─────────────┘
             │ MCP Protocol
             ▼
┌──────────────────────────┐
│        MCP Server        │
│   upstox_mcp_server.py   │
│   Registers MCP tools    │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│      Upstox Client       │
│    upstox_client.py      │
│  API requests            │
│  Input validation        │
│  Error handling          │
└────────────┬─────────────┘
             │ HTTPS + Access Token
             ▼
┌──────────────────────────┐
│        Upstox API        │
│ Account and market data  │
└──────────────────────────┘
```

---

## Project Structure

```
upstox-mcp-server/
├── .venv/                  # Local Python environment
├── .env                    # API credentials (never commit)
├── .env.example            # Example environment configuration
├── .gitignore
├── get_token.py            # OAuth authorization and token handling
├── upstox_client.py        # Upstox API client and data retrieval
├── upstox_mcp_server.py    # MCP server and tool registration
├── requirements.txt        # Python dependencies
├── upstox_token.json       # Local access token (never commit)
└── test_profile.py         # Example API test
```

> The exact files may differ as the project evolves.

---

## Prerequisites

- Python 3.10 or later
- macOS, Linux, or Windows
- [Claude Desktop](https://claude.ai/download)
- An Upstox account
- An Upstox developer application with API credentials

Useful resources:
- [Upstox Developer Portal](https://account.upstox.com/developer/apps)
- [Upstox API Documentation](https://upstox.com/developer/api-documentation/)

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/riteshsharma2406/upstox-mcp-server.git
cd upstox-mcp-server
```

### 2. Create a virtual environment

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## Upstox API Configuration

### Step 1: Create an Upstox developer application

1. Open the Upstox Developer Portal and sign in.
2. Go to the API applications section.
3. Create a new application (e.g., `Upstox MCP Server`).
4. Set the redirect URL. This project uses:
   ```
   http://localhost:3000/callback
   ```
5. Save the application.

> **Important:** The redirect URL must match the one registered with your Upstox application and the value in your local `.env`. Follow the current Upstox documentation if the portal requires a different format.

### Step 2: Get your API key and secret

Open your application's details in the portal and copy the **API Key** and **API Secret**.

| Credential   | Purpose                                                        |
|--------------|----------------------------------------------------------------|
| API Key      | Identifies your Upstox application                             |
| API Secret   | Authenticates your application during authorization            |
| Access Token | Authorizes API requests on behalf of the authenticated user    |
| Redirect URL | Where Upstox redirects the browser after authorization         |

> ⚠️ **Never** publish your API Secret or access token on GitHub, in screenshots, or in public messages.

### Step 3: Configure environment variables

```bash
cp .env.example .env
```

If `.env.example` doesn't exist, create `.env` manually and add:

```env
UPSTOX_API_KEY=your_api_key
UPSTOX_API_SECRET=your_api_secret
UPSTOX_REDIRECT_URL=http://localhost:3000/callback
```

### Step 4: Generate an access token

```bash
source .venv/bin/activate   # Windows: .venv\Scripts\Activate.ps1
python get_token.py
```

Then:
1. Open the Upstox authorization page in your browser.
2. Sign in if prompted and authorize your application.
3. Let the script exchange the authorization code for an access token.
4. Confirm the script reports successful authorization.

The token is saved locally in `upstox_token.json`. Keep this file private and out of version control.

### Step 5: Handle token expiration

Upstox access tokens have a limited lifetime. When a token expires, authenticated requests will fail. To reauthorize:

```bash
cd "/path/to/your/project"
source .venv/bin/activate
python get_token.py
```

If Claude Desktop still reports an authentication error afterward:
1. Completely quit Claude Desktop.
2. Reopen it.
3. Retry your request.

> Exact token lifetime and reauthorization rules depend on Upstox's current authentication policy.

---

## Claude Desktop Integration

### Step 1: Locate the configuration file

| OS      | Path                                                              |
|---------|-------------------------------------------------------------------|
| macOS   | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json`                     |

To open the folder:
- **macOS:** `open "$HOME/Library/Application Support/Claude"`
- **Windows:** Press `Win + R`, enter `%APPDATA%\Claude`, and press Enter.

If the file doesn't exist, check the current Claude Desktop MCP documentation before creating it.

### Step 2: Add the MCP server

Add the following to the existing `mcpServers` object. Replace the example paths with the actual absolute paths on your machine.

**macOS / Linux**
```json
{
  "mcpServers": {
    "upstox": {
      "command": "/ABSOLUTE/PATH/TO/upstox-mcp-server/.venv/bin/python",
      "args": [
        "/ABSOLUTE/PATH/TO/upstox-mcp-server/upstox_mcp_server.py"
      ]
    }
  }
}
```

**Windows** (note the escaped backslashes)
```json
{
  "mcpServers": {
    "upstox": {
      "command": "C:\\Users\\YOUR_USERNAME\\Desktop\\upstox-mcp-server\\.venv\\Scripts\\python.exe",
      "args": [
        "C:\\Users\\YOUR_USERNAME\\Desktop\\upstox-mcp-server\\upstox_mcp_server.py"
      ]
    }
  }
}
```

### Step 3: Restart Claude Desktop

1. Save `claude_desktop_config.json`.
2. Completely quit Claude Desktop.
3. Reopen it and confirm the Upstox tools are available.
4. Test the connection with:

```
Use the Upstox MCP tools to retrieve my account profile. If authentication fails, explain the error without displaying my credentials.
```

Claude Desktop launches the MCP server automatically.

### Troubleshooting

If the Upstox tools don't appear:
- Check the config file location and JSON syntax.
- Confirm the Python executable and server paths are correct.
- Make sure dependencies are installed in the configured virtual environment.
- Confirm `.env` and `upstox_token.json` exist in the project directory.
- Check whether the access token has expired.
- Restart Claude Desktop after any config change.
- Review Claude Desktop's MCP logs for startup errors.

---

## Example Prompts

Once connected, you can talk to Claude in natural language.

**Account information**
```
Use the Upstox tools to retrieve my profile and available funds. Explain the results clearly. Do not place any orders.
```

**Holdings**
```
Retrieve my current long-term holdings using the Upstox MCP tools. Summarize the returned data and identify any missing information.
```

**Market quote**
```
Search for Reliance Industries using the Upstox instrument search tool. Identify the correct instrument key and retrieve its latest available market quote.
```

**Historical analysis**
```
Retrieve the last three months of daily historical candles for a specified NSE instrument. Analyze the available price history for:
- Overall trend
- Momentum
- Volatility
- Potential support and resistance levels

Clearly distinguish observed data from interpretation. Mention the date range and any limitations in the data. Do not place any orders.
```

**Stock research**
```
Help me research potentially promising NSE stocks. Use available Upstox tools to retrieve relevant quotes and historical data. Explain the observed trends, potential risks, and uncertainties. Identify any missing information, such as company fundamentals, valuation, earnings, or recent news, that would be needed for a more complete assessment. Do not guarantee returns or place any orders. Present the results as research candidates, not guaranteed profitable stocks.
```

> **Note:** This project does not include a market-wide screening engine or complete fundamental and news data. Claude's research is limited by the available tools and any additional sources it can access. Historical prices and technical indicators cannot guarantee future returns.

---

## Development and Testing

```bash
# Activate the virtual environment
source .venv/bin/activate

# Check Python syntax
python -m py_compile get_token.py upstox_client.py upstox_mcp_server.py

# Run the profile test (requires valid credentials and a usable access token)
python test_profile.py
```

Guidelines:
- Don't print API secrets, access tokens, or full authentication responses while debugging.
- When using MCP's stdio transport, **don't print debug messages to standard output**, as this can break MCP communication. Log to standard error instead.

---

## Security Considerations

- Never commit `.env` or `upstox_token.json`
- Never hardcode API secrets or access tokens in source code
- Keep your virtual environment out of version control
- Use HTTPS for all API requests
- Validate user-supplied tool arguments
- Handle authentication errors without exposing credentials
- Avoid logging sensitive account information unnecessarily
- Review staged files before pushing to GitHub
- If credentials are exposed, revoke or regenerate them following Upstox's procedures

---

## Current Limitations

- Read-only data access; order placement and trade execution are not implemented
- No market-wide stock screening
- No dedicated fundamentals or news integrations
- Research quality depends on the completeness and freshness of available data
- Expired access tokens require renewed authorization
- No investment returns are guaranteed

---

## Roadmap

- [ ] Complete and validate intraday candle retrieval
- [ ] Expand automated tests for API responses and errors
- [ ] Improve token-expiration handling
- [ ] Improve error messages and diagnostic logging
- [ ] Improve installation and configuration documentation
- [ ] Add broader stock discovery and screening capabilities
- [ ] Explore integrations for company fundamentals and market news
- [ ] Consider optional trading functionality with explicit confirmation, risk checks, and audit logging

---

## Disclaimer

This project is intended for educational, development, and research purposes only. It is **not financial advice** and does not guarantee investment returns. Verify market data and investment decisions independently.

The current implementation is read-only and does not execute trades. Any future trading functionality should include appropriate safeguards, risk controls, and explicit authorization.
