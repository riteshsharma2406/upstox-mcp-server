from mcp.server.fastmcp import FastMCP

from upstox_client import create_client


mcp = FastMCP("Upstox MCP")


@mcp.tool()
def get_profile() -> dict:
    """Retrieve the authenticated user's Upstox profile.

    Returns account configuration such as enabled exchanges and
    permitted order types. Does not place trades or modify the account.
    """

    client = None

    try:
        client = create_client()
        profile = client.get_profile()

        return profile

    except RuntimeError as exc:
        return {
            "status": "error",
            "message": str(exc),
        }

    finally:
        if client is not None:
            client.close()

@mcp.tool()
def get_funds() -> dict:
    """Retrieve the authenticated user's available funds and margin from Upstox.

    Returns account funds information directly from Upstox.
    This tool is read-only and does not place or modify orders.
    """
    client = None

    try:
        client = create_client()
        funds = client.get_funds()
        return funds

    except RuntimeError as exc:
        return {
            "status": "error",
            "message": str(exc),
        }

    finally:
        if client is not None:
            client.close()

@mcp.tool()
def get_holdings() -> dict:
    """Retrieve the user's long-term stock holdings from Upstox.

    Returns stock holdings directly from Upstox, including quantities,
    average prices, market prices, and broker-reported P&L.
    This tool is read-only and does not modify the account.
    """
    client = None

    try:
        client = create_client()
        return client.get_holdings()

    except RuntimeError as exc:
        return {
            "status": "error",
            "message": str(exc),
        }

    finally:
        if client is not None:
            client.close()

@mcp.tool()
def get_positions() -> dict:
    """Retrieve the user's current trading positions from Upstox.

    Returns position data, including quantities, prices, and
    broker-reported profit/loss when available.
    This tool is read-only and does not modify positions.
    """
    client = None

    try:
        client = create_client()
        return client.get_positions()

    except RuntimeError as exc:
        return {
            "status": "error",
            "message": str(exc),
        }

    finally:
        if client is not None:
            client.close()

@mcp.tool()
def get_orders() -> dict:

    client = None
    try:
        client = create_client()
        return client.get_orders()
    
    except RuntimeError as exc:
        return {

            "status": "error",

            "message": str(exc),

        }
    finally:
        if client is not None:
            client.close()

@mcp.tool()
def get_market_quote(instrument_key: str) -> dict:
    client = None

    try:
        client = create_client()
        return client.get_market_quote(instrument_key)
    except (RuntimeError, ValueError) as exc:
        return {
            "status": "error",
            "message": str(exc),
    }
    finally:
        if client is not None:
            client.close()

@mcp.tool()
def search_instrument(query: str, exchange: str = "NSE", segment: str = "EQ", page_number: int = 1, records: int = 10) -> dict:
    client = None
    try:
        client = create_client()
        return client.search_instrument(
            query=query,
            exchange=exchange,
            segment=segment,
            page_number=page_number,
            records=records,
        )
    except (RuntimeError, ValueError) as exc:
        return {
            "status": "error",
            "message": str(exc),
        }
    finally:
        if client is not None:
            client.close()


@mcp.tool()
def get_historical_candles(
    instrument_key: str,
    unit: str,
    interval: int,
    from_date: str,
    to_date: str,
) -> dict:
    client = None

    try:
        client = create_client()
        return client.get_historical_candles(
            instrument_key=instrument_key,
            unit=unit,
            interval=interval,
            from_date=from_date,
            to_date=to_date,
        )
    except (RuntimeError, ValueError) as exc:
        return {
            "status": "error",
            "message": str(exc),
        }
    finally:
        if client is not None:
            client.close()


if __name__ == "__main__":
    mcp.run(transport="stdio")