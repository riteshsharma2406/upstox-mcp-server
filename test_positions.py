import json
from upstox_client import create_client


def main():
    client = create_client()

    try:
        print("Fetching positions from Upstox...")

        positions = client.get_positions()

        if positions.get("status") != "success":
            print("API returned an unsuccessful response.")
            print(json.dumps(positions, indent=2))
            return

        data = positions.get("data", [])

        print("\nAPI request successful!")
        print(f"Number of positions returned: {len(data)}")
        print("\nPositions response:")
        print(json.dumps(positions, indent=2))

    except RuntimeError as exc:
        print(f"API request failed: {exc}")

    finally:
        client.close()


if __name__ == "__main__":
    main()