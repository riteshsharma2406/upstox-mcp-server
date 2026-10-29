import json
from upstox_client import create_client


def main():
    client = create_client()

    try:
        print("Fetching stock holdings from Upstox...")

        holdings = client.get_holdings()

        if holdings.get("status") != "success":
            print("API returned an unsuccessful response.")
            print(json.dumps(holdings, indent=2))
            return

        data = holdings.get("data", [])

        print("\nAPI request successful!")
        print(f"Number of holdings returned: {len(data)}")
        print("\nHoldings response:")
        print(json.dumps(holdings, indent=2))

    except RuntimeError as exc:
        print(f"API request failed: {exc}")

    finally:
        client.close()


if __name__ == "__main__":
    main()