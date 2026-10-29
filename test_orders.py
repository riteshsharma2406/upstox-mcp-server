import json
from upstox_client import create_client


def main():
    client = create_client()

    try:
        print("Fetching today's orders from Upstox...")

        orders = client.get_orders()

        if orders.get("status") != "success":
            print("API returned an unsuccessful response.")
            print(json.dumps(orders, indent=2))
            return

        data = orders.get("data", [])

        print("\nAPI request successful!")
        print(f"Number of orders returned: {len(data)}")
        print("\nOrders response:")
        print(json.dumps(orders, indent=2))

    except RuntimeError as exc:
        print(f"API request failed: {exc}")

    finally:
        client.close()


if __name__ == "__main__":
    main()