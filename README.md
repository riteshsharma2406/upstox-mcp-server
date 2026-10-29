Upstox MCP Server

A Python-based Model Context Protocol (MCP) server that connects Claude Desktop to the Upstox API, enabling AI-assisted access to Indian stock market data and trading account information.

The project demonstrates how to integrate financial APIs with AI assistants using Python, OAuth authentication, and MCP tools.

Current scope: Read-only access to account information and market data. Order placement and trade execution are not implemented.

Features

Account Information

* Retrieve the authenticated user’s profile.
* Retrieve funds and margin information.
* View long-term holdings.
* Retrieve current trading positions.
* View the order book.

Market Data

* Search for supported market instruments.
* Retrieve market quotes for specified instruments.
* Fetch historical candlestick data.
* Retrieve intraday candlestick data when the corresponding tool is implemented and enabled.

AI Integration

* Connect Upstox API tools to Claude Desktop using MCP.
* Retrieve financial data through natural-language prompts.
* Support AI-assisted stock research using market quotes and historical prices.
* Separate API data retrieval from AI interpretation and analysis.

Authentication

* OAuth-based Upstox authorization.
* Local storage of the access token.
* Reauthorization when the access token expires.

Tech Stack

* Language: Python
* AI integration: Model Context Protocol (MCP)
* MCP framework: FastMCP
* HTTP client: HTTPX
* Authentication: Upstox OAuth
* Configuration: python-dotenv
* AI assistant: Claude Desktop
* Market data provider: Upstox API

Architecture

                  ┌────────────────────────┐
                  │     Claude Desktop     │
                  │                        │
                  │Natural-language prompts│
                  └───────────┬────────────┘
                              │
                              │ MCP Protocol
                              ▼
                  ┌────────────────────────┐
                  │       MCP Server       │
                  │ upstox_mcp_server.py   │
                  │                        │
                  │ Registers MCP tools    │
                  └───────────┬────────────┘
                              │
                              ▼
                  ┌────────────────────────┐
                  │     Upstox Client      │
                  │    upstox_client.py    │
                  │                        │
                  │ API requests           │
                  │ Input validation       │
                  │ Error handling         │
                  └───────────┬────────────┘
                              │
                              │ HTTPS + Access Token
                              ▼
                  ┌────────────────────────┐
                  │       Upstox API       │
                  │                        │
                  │ Account and market data│
                  └────────────────────────┘

Project Structure

Upstox MCP/
├── .venv/                    # Local Python environment
├── .env                      # API credentials (never commit)
├── .env.example              # Example environment configuration
├── .gitignore
├── get_token.py              # OAuth authorization and token handling
├── upstox_client.py          # Upstox API client and data retrieval
├── upstox_mcp_server.py      # MCP server and tool registration
├── requirements.txt          # Python dependencies
├── upstox_token.json         # Local access token (never commit)
└── test_profile.py           # Example API test

The exact files may differ as the project evolves.

Prerequisites

Before getting started, you need:

* Python 3.10 or later.
* A macOS, Linux, or other supported Python environment.
* Claude Desktop.
* An Upstox account.
* An Upstox developer application with API credentials.

Useful resources:

* Upstox Developer Portal
* Upstox API Documentation
* Claude Desktop

Installation

1. Clone the Repository

git clone https://github.com/riteshsharma2406/upstox-mcp-server.git
cd upstox-mcp-server

2. Create a Virtual Environment

On macOS or Linux:

python3 -m venv .venv
source .venv/bin/activate

3. Install Dependencies

python -m pip install --upgrade pip
pip install -r requirements.txt

Upstox API Configuration

Before running the project, create an Upstox developer application and configure its credentials.

Step 1: Create an Upstox Developer Application

1. Open the Upstox Developer Portal.
2. Sign in with your Upstox account.
3. Navigate to the API applications section.
4. Create a new application.
5. Enter an application name, such as Upstox MCP Server.
6. Configure the redirect URL.
7. Save your application.

For this project, the example redirect URL is:

http://localhost:3000/callback

Important: The redirect URL must match the URL registered with your Upstox application and the value configured in your local environment. Follow the current Upstox documentation if the portal requires a different format or additional configuration.

Step 2: Obtain Your API Key and API Secret

After creating your application:

1. Open the application details in the Upstox Developer Portal.
2. Locate the API Key and API Secret.
3. Copy these credentials for local configuration.

What are these credentials?

Credential	Purpose
API Key	Identifies your Upstox application.
API Secret	Used during the authorization process to authenticate your application.
Access Token	Authorizes API requests on behalf of the authenticated user.
Redirect URL	Specifies where Upstox redirects the browser after authorization.

Security warning: Never publish your API Secret or access token on GitHub, in screenshots, or in public messages.

Step 3: Configure Environment Variables

Create your local .env file from the example:

cp .env.example .env

If .env.example does not exist in the repository, create .env manually.

Open .env and configure your credentials:

UPSTOX_API_KEY=your_api_key
UPSTOX_API_SECRET=your_api_secret
UPSTOX_REDIRECT_URL=http://localhost:3000/callback

Replace the example values with your actual application credentials.

Make sure the redirect URL matches your registered Upstox application configuration.

Step 4: Generate an Access Token

Activate the virtual environment if it is not already active:

source .venv/bin/activate

Run the authentication script:

python get_token.py

Follow the authorization process in your browser:

1. Open the Upstox authorization page.
2. Sign in if prompted.
3. Authorize your application.
4. Allow the script to exchange the authorization code for an access token.
5. Confirm that the script reports successful authorization.

The project saves the access token locally in:

upstox_token.json

Keep this file private and exclude it from version control.

Step 5: Handle Access Token Expiration

Upstox access tokens have a limited lifetime. When a token expires, authenticated requests may fail.

To authorize again, run:

cd "/path/to/your/project"
source .venv/bin/activate
python get_token.py

Complete the authorization flow and allow the script to save the new token.

If Claude Desktop still reports an authentication error afterward:

1. Completely quit Claude Desktop.
2. Reopen Claude Desktop.
3. Retry your request.

The exact token lifetime and reauthorization requirements depend on Upstox’s current authentication rules.

Claude Desktop Integration

After configuring your Upstox API credentials and generating an access token, connect the MCP server to Claude Desktop.

Step 1: Locate the Claude Desktop Configuration File

The configuration file location depends on your operating system.

macOS

~/Library/Application Support/Claude/claude_desktop_config.json

To open the configuration directory in Finder, run:

open "$HOME/Library/Application Support/Claude"

Windows

%APPDATA%\Claude\claude_desktop_config.json

To open the configuration directory in File Explorer, press Win + R, enter:

%APPDATA%\Claude

Then press Enter.

If the configuration file does not exist, check the current Claude Desktop MCP setup documentation before creating it.

Step 2: Configure the MCP Server

Add the Upstox MCP server to the existing mcpServers object in claude_desktop_config.json.

macOS example

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

Replace the example paths with the actual absolute paths on your Mac.

For example, if your project is located in your Desktop folder:

{
  "mcpServers": {
    "upstox": {
      "command": "/Users/YOUR_USERNAME/Desktop/Upstox MCP/.venv/bin/python",
      "args": [
        "/Users/YOUR_USERNAME/Desktop/Upstox MCP/upstox_mcp_server.py"
      ]
    }
  }
}

Windows example

If your project is located at C:\Users\YOUR_USERNAME\Desktop\upstox-mcp-server, configure:

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

Replace YOUR_USERNAME and the example project paths with the actual paths on your computer.

Step 3: Install Dependencies

Before starting Claude Desktop, make sure the project’s dependencies are installed in its virtual environment.

macOS

cd "/path/to/upstox-mcp-server"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

Windows — PowerShell

cd "C:\path\to\upstox-mcp-server"
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt

If the virtual environment already exists and is configured correctly, you do not need to recreate it.

Step 4: Configure Upstox Credentials

Create a .env file using .env.example and add your Upstox API credentials.

UPSTOX_API_KEY=your_api_key
UPSTOX_API_SECRET=your_api_secret
UPSTOX_REDIRECT_URL=http://localhost:3000/callback

Generate an access token by running:

python get_token.py

Complete the Upstox authorization process.

Keep .env and upstox_token.json private. Never commit them to GitHub.

Step 5: Restart Claude Desktop

1. Save claude_desktop_config.json.
2. Completely quit Claude Desktop.
3. Reopen Claude Desktop.
4. Check that the Upstox MCP tools are available.
5. Test the connection with the prompt below.

Use the Upstox MCP tools to retrieve my account profile.
If authentication fails, explain the error without displaying my credentials.

Claude Desktop should launch the configured MCP server automatically.

Troubleshooting

If the Upstox tools are unavailable:

* Verify the configuration file’s location and JSON syntax.
* Confirm that the Python executable and server paths are correct.
* Ensure dependencies are installed in the configured virtual environment.
* Confirm that .env and upstox_token.json exist in the project directory.
* Check whether the access token has expired.
* Restart Claude Desktop after changing the configuration.
* Review Claude Desktop’s MCP logs for startup errors.

For the latest platform-specific instructions, consult the Claude documentation and the Upstox API documentation.

Example Prompts for Claude

Once the server is connected, you can interact with Claude using natural language.

1. Retrieve Account Information

Use the Upstox tools to retrieve my profile and available funds.
Explain the results clearly. Do not place any orders.

2. Retrieve Holdings

Retrieve my current long-term holdings using the Upstox MCP tools.
Summarize the returned data and identify any missing information.

3. Retrieve a Market Quote

Search for Reliance Industries using the Upstox instrument search tool.
Identify the correct instrument key and retrieve its latest available market quote.

4. Analyze Historical Prices

Retrieve the last three months of daily historical candles for a specified NSE instrument.
Analyze the available price history for:
- Overall trend
- Momentum
- Volatility
- Potential support and resistance levels
Clearly distinguish observed data from interpretation.
Mention the date range and any limitations in the data.
Do not place any orders.

5. Research Potential Stock Opportunities

Help me research potentially promising NSE stocks.
Use available Upstox tools to retrieve relevant quotes and historical data.
Explain the observed trends, potential risks, and uncertainties.
Identify any missing information, such as company fundamentals, valuation,
earnings, or recent news, that would be needed for a more complete assessment.
Do not guarantee returns or place any orders.
Present the results as research candidates, not guaranteed profitable stocks.

Important: The current project does not provide a comprehensive market-wide screening engine or complete fundamental and news data. Claude’s research is limited by the available tools and any additional sources it can access.

Historical prices and technical indicators cannot guarantee future returns.

Development and Testing

Activate the Virtual Environment

source .venv/bin/activate

Check Python Syntax

python -m py_compile get_token.py upstox_client.py upstox_mcp_server.py

Run the Profile Test

python test_profile.py

Run tests only after configuring valid credentials and a usable access token.

Do not print API secrets, access tokens, or complete authentication responses during debugging.

MCP Standard Output

When running with MCP’s standard input/output transport, avoid printing debugging messages to standard output. Such messages can interfere with MCP communication.

Use appropriate logging to standard error when debugging the server.

Security Considerations

* Never commit .env.
* Never commit upstox_token.json.
* Never hardcode API secrets or access tokens in source code.
* Keep your virtual environment out of version control.
* Use HTTPS for API requests.
* Validate user-supplied tool arguments.
* Handle authentication errors without exposing credentials.
* Avoid logging sensitive account information unnecessarily.
* Review staged files before pushing to GitHub.
* If credentials are exposed, follow Upstox’s credential revocation or regeneration procedures.

Current Limitations

* The server currently focuses on read-only data access.
* Order placement and trade execution are not implemented.
* Comprehensive market-wide stock screening is not implemented.
* Fundamental data and news integrations are not included as dedicated project features.
* Research quality depends on the completeness and freshness of available data.
* Expired access tokens require renewed authorization.
* No investment returns are guaranteed.

Roadmap

* Complete and validate intraday candle retrieval.
* Expand automated tests for API responses and errors.
* Improve token-expiration handling.
* Improve error messages and diagnostic logging.
* Improve installation and configuration documentation.
* Add broader stock discovery and screening capabilities.
* Explore integrations for company fundamentals and market news.
* Consider optional trading functionality with explicit confirmation, risk checks, and audit logging.

Disclaimer

This project is intended for educational, development, and research purposes.

It is not financial advice and does not guarantee investment returns. Verify market data and investment decisions independently.

The current implementation is read-only and does not execute trades. Any future trading functionality should incorporate appropriate safeguards, risk controls, and explicit authorization.
