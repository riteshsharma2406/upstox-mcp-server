import json
from upstox_client import create_client


def main():
    instrument_key = input(
        "Enter an Upstox instrument key (for example, NSE_EQ|INE848E01016): "
    ).strip()

    if not instrument_key:
        print("Instrument key cannot be empty.")
        return

    client = create_client()

    try:
        print(f"\nFetching market quote for {instrument_key}...")

        quote = client.get_market_quote(instrument_key)

        if quote.get("status") != "success":
            print("API returned an unsuccessful response.")
            print(json.dumps(quote, indent=2))
            return

        print("\nAPI request successful!")
        print("\nMarket quote response:")
        print(json.dumps(quote, indent=2))

    except (RuntimeError, ValueError) as exc:
        print(f"API request failed: {exc}")

    finally:
        client.close()


if __name__ == "__main__":
    main()