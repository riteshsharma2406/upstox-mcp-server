import json
from upstox_client import create_client


def main():
    client = create_client()

    try:
        print("Fetching funds from Upstox...")

        funds = client.get_funds()

        if funds.get("status") != "success":
            print("API returned an unsuccessful response.")
            print(json.dumps(funds, indent=2))
            return

        print("\nAPI request successful!")
        print("\nFunds response:")
        print(json.dumps(funds, indent=2))

    except RuntimeError as exc:
        print(f"API request failed: {exc}")

    finally:
        client.close()


if __name__ == "__main__":
    main()