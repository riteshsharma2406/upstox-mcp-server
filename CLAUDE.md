Upstox MCP Trading Assistant

Project Overview

Build a Python MCP server that connects Claude Desktop and Claude Code to the Upstox trading account through the official Upstox API v2/v3.

The application provides read-only market data and portfolio tools first, followed by analytics, risk management, alerts, journaling, and backtesting in later phases.

Python 3.10+ is required.

Development Workflow

1. Work strictly in the currently approved phase.
2. Implement one small step at a time.
3. Run relevant tests before proceeding.
4. Explain what changed and how to verify it.
5. Stop after completing each phase and wait for explicit approval before starting the next phase.
6. Make small, reviewable Git commits at appropriate milestones.
7. Do not rewrite or delete working functionality without a clear reason.

Mandatory API Documentation Rules

* Consult the current official documentation at https://upstox.com/developer/api-documentation before implementing an Upstox API integration.
* Verify every endpoint’s HTTP method, URL, headers, parameters, request body, and response structure.
* Use official Upstox API v2/v3 endpoints as appropriate.
* Never invent endpoints, fields, response shapes, or authentication behavior.
* If the documentation is ambiguous, stop and explain the uncertainty.
* Mock API responses in tests wherever possible.

Security Rules

* Load secrets exclusively from .env.
* Never hardcode, print, or log API secrets, access tokens, authorization codes, or other credentials.
* Keep .env, upstox_token.json, venv/, .venv/, database files, and trades.log out of Git.
* Store the access token locally in upstox_token.json.
* If authentication is missing or expired, provide a clear instruction to run python get_token.py.
* Validate all tool inputs.
* Never expose raw stack traces to MCP clients.
* Never execute a real trade unintentionally.
* All future order placement must pass through risk.py.
* Default DRY_RUN=true.
* Never implement order-placement tools before the order-execution phase is approved.

MCP Server Rules

* Use the official Python MCP SDK and FastMCP.
* Use stdio transport for Claude Desktop and Claude Code.
* Never print diagnostic output to stdout because it can corrupt MCP protocol communication.
* Send diagnostics to stderr or an appropriate log file.
* Keep upstox_mcp_server.py thin. Put API, authentication, instrument, analysis, risk, and persistence logic in separate modules.
* Every MCP tool must have a clear docstring, typed parameters, input validation, and graceful error handling.
* Return clean, structured, readable JSON-compatible results.

Approved Project Layout

* upstox_mcp_server.py: MCP tool registration.
* get_token.py: OAuth authorization flow.
* upstox_client.py: API wrapper and authentication handling.
* instruments.py: instrument master download, caching, and search.
* analysis.py: market analysis and technical indicators.
* risk.py: risk limits, position sizing, and order validation.
* storage.py: SQLite persistence for watchlists, alerts, and journals.
* tests/: automated tests.
* requirements.txt: approved dependencies.
* .env.example: configuration template without real credentials.
* README.md: setup and usage instructions.

Approved Dependencies

Use Python’s standard library and the following approved packages as needed:

* mcp
* httpx
* python-dotenv
* pandas
* pandas-ta
* pytest

Ask for approval before adding any dependency not listed above.

Testing Requirements

* Use pytest.
* Mock Upstox HTTP responses in unit tests.
* Test successful requests, invalid inputs, timeouts, authentication errors, and API errors.
* Test risk limits and rejection paths before enabling order execution.
* Never require a real order or financial transaction to run automated tests.

Phase Boundaries

Phase 1

Authentication, API wrapper, instrument search, and nine read-only tools.

Phase 2

Historical candles, technical indicators, support/resistance, option chain, and market overview.

Phase 3

Portfolio summary, trade history, realized P&L, and risk exposure.

Phase 4

Risk controls and order execution, including dry-run behavior and append-only audit logging.

Phase 5

Watchlists, price alerts, and monitoring.

Phase 6

Trade journal, strategy backtesting, and MCP prompts.

Do not start a later phase without explicit user approval.