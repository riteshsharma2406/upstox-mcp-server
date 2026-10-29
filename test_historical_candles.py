import json
from upstox_client import create_client


def main():
    instrument_key = input("Enter the Upstox instrument key: ").strip()
    from_date = input("Enter start date (YYYY-MM-DD): ").strip()
    to_date = input("Enter end date (YYYY-MM-DD): ").strip()

    client = create_client()

    try:
        print("\nFetching historical daily candles...")

        result = client.get_historical_candles(
            instrument_key=instrument_key,
            unit="days",
            interval=1,
            from_date=from_date,
            to_date=to_date,
        )

        if result.get("status") != "success":
            print("API returned an unsuccessful response.")
            print(json.dumps(result, indent=2))
            return

        candles = result.get("data", {}).get("candles", [])

        print("\nAPI request successful!")
        print(f"Number of candles returned: {len(candles)}")
        print("\nHistorical candle response:")
        print(json.dumps(result, indent=2))

    except (RuntimeError, ValueError) as exc:
        print(f"Request failed: {exc}")

    finally:
        client.close()


if __name__ == "__main__":
    main()