from upstox_client import create_client

def main():
    client = create_client()
    try:
        profile = client.get_profile()

        print("API request successful!")
        print("Response status:", profile.get("status"))

        data = profile.get("data", {})

        print("Broker:", data.get("broker"))
        print("Enabled exchanges:", data.get("exchanges"))
        print("Enabled order types:", data.get("order_types"))

    except RuntimeError as exc:
        print("API request failed:", str(exc))

    finally:
        client.close()


if __name__ == "__main__":
    main()