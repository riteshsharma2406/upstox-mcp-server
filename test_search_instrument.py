import json
from upstox_client import create_client


def main():
    query = input("Enter a company name or trading symbol: ").strip()

    if not query:
        print("Search query cannot be empty.")
        return

    client = create_client()

    try:
        print(f"\nSearching Upstox for: {query}")

        result = client.search_instrument(
            query=query,
            exchange="NSE",
            segment="EQ",
            records=10,
        )

        if result.get("status") != "success":
            print("API returned an unsuccessful response.")
            print(json.dumps(result, indent=2))
            return

        instruments = result.get("data", [])

        print("\nAPI request successful!")
        print(f"Matching instruments: {len(instruments)}")
        print("\nSearch results:")
        print(json.dumps(result, indent=2))

    except (RuntimeError, ValueError) as exc:
        print(f"Search failed: {exc}")

    finally:
        client.close()


if __name__ == "__main__":
    main()