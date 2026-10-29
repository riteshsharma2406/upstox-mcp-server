import httpx

from get_token import load_token
from urllib.parse import quote


BASE_URL = "https://api.upstox.com/v2"


class UpstoxClient:
    """Client for making authenticated Upstox API requests."""

    def __init__(self, access_token: str):
        if not access_token:
            raise ValueError("Access token is missing.")

        self.client = httpx.Client(
            base_url=BASE_URL,
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {access_token}",
            },
            timeout=20.0,
        )

    def get_profile(self) -> dict:
        """Retrieve the authenticated Upstox user's profile."""

        try:
            response = self.client.get("/user/profile")
            response.raise_for_status()

        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 401:
                raise RuntimeError(
                    "Authentication failed. Your access token may have expired. "
                    "Run python get_token.py to authorize again."
                ) from None

            raise RuntimeError(
                f"Upstox profile request failed with HTTP status "
                f"{exc.response.status_code}."
            ) from None

        except httpx.RequestError:
            raise RuntimeError(
                "Could not connect to Upstox. Check your internet connection."
            ) from None

        try:
            result = response.json()
        except ValueError:
            raise RuntimeError(
                "Upstox returned an invalid JSON response."
            ) from None

        if not isinstance(result, dict):
            raise RuntimeError("Unexpected response format from Upstox.")

        return result

    def close(self) -> None:
        """Close the HTTP client and release its resources."""

        self.client.close()

    def get_funds(self) -> dict:
        """Retrieve the user's available funds and margin from Upstox."""
        try:
            response = self.client.get(
                "https://api.upstox.com/v3/user/get-funds-and-margin",
                headers={"Api-Version": "3.0"},
            )
            response.raise_for_status()

        except httpx.HTTPStatusError as exc:
            status_code = exc.response.status_code

            if status_code == 401:
                raise RuntimeError(
                    "Authentication failed. Your access token may have expired. "
                    "Run python get_token.py to authorize again."
                ) from None

            if status_code == 423:
                raise RuntimeError(
                    "The Upstox funds service is temporarily unavailable. "
                    "It may be in its scheduled maintenance window."
                ) from None

            raise RuntimeError(
                f"Upstox funds request failed with HTTP status {status_code}."
            ) from None

        except httpx.RequestError:
            raise RuntimeError(
                "Could not connect to Upstox. Check your internet connection."
            ) from None

        try:
            result = response.json()
        except ValueError:
            raise RuntimeError(
                "Upstox returned an invalid JSON response."
            ) from None

        if not isinstance(result, dict):
            raise RuntimeError("Unexpected response format from Upstox.")

        return result

    def get_holdings(self) -> dict:
        """Retrieve the user's long-term stock holdings from Upstox."""
        try:
            response = self.client.get(
                "/portfolio/long-term-holdings"
            )
            response.raise_for_status()

        except httpx.HTTPStatusError as exc:
            status_code = exc.response.status_code

            if status_code == 401:
                raise RuntimeError(
                    "Authentication failed. Your access token may have expired. "
                    "Run python get_token.py to authorize again."
                ) from None

            raise RuntimeError(
                f"Upstox holdings request failed with HTTP status {status_code}."
            ) from None

        except httpx.RequestError:
            raise RuntimeError(
                "Could not connect to Upstox. Check your internet connection."
            ) from None

        try:
            result = response.json()
        except ValueError:
            raise RuntimeError(
                "Upstox returned an invalid JSON response."
            ) from None

        if not isinstance(result, dict):
            raise RuntimeError("Unexpected response format from Upstox.")

        return result

    def get_positions(self) -> dict:
        """Retrieve the user's current trading positions from Upstox."""
        try:
            response = self.client.get(
                "/portfolio/short-term-positions"
            )
            response.raise_for_status()

        except httpx.HTTPStatusError as exc:
            status_code = exc.response.status_code

            if status_code == 401:
                raise RuntimeError(
                    "Authentication failed. Your access token may have expired. "
                    "Run python get_token.py to authorize again."
                ) from None

            raise RuntimeError(
                f"Upstox positions request failed with HTTP status {status_code}."
            ) from None

        except httpx.RequestError:
            raise RuntimeError(
                "Could not connect to Upstox. Check your internet connection."
            ) from None

        try:
            result = response.json()
        except ValueError:
            raise RuntimeError(
                "Upstox returned an invalid JSON response."
            ) from None

        if not isinstance(result, dict):
            raise RuntimeError("Unexpected response format from Upstox.")

        return result

    def get_orders(self) -> dict:
        """Retrieve the current day's order book from Upstox."""
        try:
            response = self.client.get("/order/retrieve-all")
            response.raise_for_status()

        except httpx.HTTPStatusError as exc:
            status_code = exc.response.status_code

            if status_code == 401:
                raise RuntimeError(
                    "Authentication failed. Your access token may have expired. "
                    "Run python get_token.py to authorize again."
                ) from None

            raise RuntimeError(
                f"Upstox orders request failed with HTTP status {status_code}."
            ) from None

        except httpx.RequestError:
            raise RuntimeError(
                "Could not connect to Upstox. Check your internet connection."
            ) from None

        try:
            result = response.json()
        except ValueError:
            raise RuntimeError(
                "Upstox returned an invalid JSON response."
            ) from None

        if not isinstance(result, dict):
            raise RuntimeError("Unexpected response format from Upstox.")

        return result

    def get_market_quote(self, instrument_key: str) -> dict:
        """Retrieve the full market quote for an Upstox instrument."""

        if not isinstance(instrument_key, str) or not instrument_key.strip():
            raise ValueError("instrument_key must be a non-empty string.")

        try:
            response = self.client.get(
                "/market-quote/quotes",
                params={"instrument_key": instrument_key.strip()},
            )
            response.raise_for_status()

        except httpx.HTTPStatusError as exc:
            status_code = exc.response.status_code

            if status_code == 401:
                raise RuntimeError(
                    "Authentication failed. Your access token may have expired. "
                    "Run python get_token.py to authorize again."
                ) from None

            raise RuntimeError(
                f"Upstox market quote request failed with HTTP status {status_code}."
            ) from None

        except httpx.RequestError:
            raise RuntimeError(
                "Could not connect to Upstox. Check your internet connection."
            ) from None

        try:
            result = response.json()
        except ValueError:
            raise RuntimeError(
                "Upstox returned an invalid JSON response."
            ) from None

        if not isinstance(result, dict):
            raise RuntimeError("Unexpected response format from Upstox.")

        return result

    def search_instrument(
        self,
        query: str,
        exchange: str = "NSE",
        segment: str = "EQ",
        page_number: int = 1,
        records: int = 10,
    ) -> dict:
        """Search for instruments by name, symbol, or ISIN."""

        if not isinstance(query, str) or not query.strip():
            raise ValueError("Search query cannot be empty.")

        if len(query.strip()) > 50:
            raise ValueError("Search query cannot exceed 50 characters.")

        if exchange not in {"ALL", "NSE", "BSE", "MCX"}:
            raise ValueError("Exchange must be ALL, NSE, BSE, or MCX.")

        if segment not in {
            "ALL", "EQ", "FO", "CURR", "COMM", "INDEX", "OPT", "FUT"
        }:
            raise ValueError("Invalid segment.")

        if isinstance(page_number, bool) or not isinstance(page_number, int) or page_number < 1:
            raise ValueError("page_number must be an integer greater than or equal to 1.")

        if isinstance(records, bool) or not isinstance(records, int) or not 1 <= records <= 30:
            raise ValueError("records must be an integer between 1 and 30.")

        params = {
            "query": query.strip(),
            "exchanges": exchange,
            "segments": segment,
            "page_number": page_number,
            "records": records,
        }

        try:
            response = self.client.get(
                "/instruments/search",
                params=params,
            )
            response.raise_for_status()

        except httpx.HTTPStatusError as exc:
            status_code = exc.response.status_code

            if status_code == 401:
                raise RuntimeError(
                    "Authentication failed. Your access token may have expired. "
                    "Run python get_token.py to authorize again."
                ) from None

            raise RuntimeError(
                f"Upstox instrument search failed with HTTP status {status_code}."
            ) from None

        except httpx.RequestError:
            raise RuntimeError(
                "Could not connect to Upstox. Check your internet connection."
            ) from None

        try:
            result = response.json()
        except ValueError:
            raise RuntimeError(
                "Upstox returned an invalid JSON response."
            ) from None

        if not isinstance(result, dict):
            raise RuntimeError("Unexpected response format from Upstox.")

        return result

    def get_historical_candles(
        self,
        instrument_key: str,
        unit: str,
        interval: int,
        to_date: str,
        from_date: str,
    ) -> dict:
        """Retrieve historical candles directly from Upstox."""

        from datetime import date

        if not isinstance(instrument_key, str) or not instrument_key.strip():
            raise ValueError("instrument_key must be a non-empty string.")

        if unit not in {"minutes", "hours", "days", "weeks", "months"}:
            raise ValueError(
                "unit must be minutes, hours, days, weeks, or months."
            )

        if isinstance(interval, bool) or not isinstance(interval, int):
            raise ValueError("interval must be an integer.")

        if unit == "minutes" and not 1 <= interval <= 300:
            raise ValueError("Minute interval must be between 1 and 300.")

        if unit == "hours" and not 1 <= interval <= 5:
            raise ValueError("Hour interval must be between 1 and 5.")

        if unit in {"days", "weeks", "months"} and interval != 1:
            raise ValueError(
                "Daily, weekly, and monthly intervals must be 1."
            )

        try:
            start_date = date.fromisoformat(from_date)
            end_date = date.fromisoformat(to_date)
        except (TypeError, ValueError):
            raise ValueError("Dates must use YYYY-MM-DD format.") from None

        if start_date > end_date:
            raise ValueError("from_date must be on or before to_date.")

        encoded_instrument_key = quote(instrument_key.strip(), safe="")

        endpoint = (
            f"https://api.upstox.com/v3/historical-candle/"
            f"{encoded_instrument_key}/"
            f"{unit}/{interval}/{to_date}/{from_date}"
        )

        try:
            response = self.client.get(
                endpoint,
                headers={"Api-Version": "3.0"},
            )
            # print("DEBUG historical URL:", endpoint)
            response.raise_for_status()

        except httpx.HTTPStatusError as exc:
            status_code = exc.response.status_code
            try:
                error_body = exc.response.json()
            except ValueError:
                error_body = exc.response.text[:500]

            if status_code == 401:
                raise RuntimeError(
                    "Authentication failed. Your access token may have expired. "
                    "Run python get_token.py to authorize again."
                ) from None

            raise RuntimeError(
                f"Upstox historical candles request failed with "
                f"HTTP status {status_code}."
                f"Response: {error_body}"
            ) from None

        except httpx.RequestError:
            raise RuntimeError(
                "Could not connect to Upstox. Check your internet connection."
            ) from None

        try:
            result = response.json()
        except ValueError:
            raise RuntimeError(
                "Upstox returned an invalid JSON response."
            ) from None

        if not isinstance(result, dict):
            raise RuntimeError("Unexpected response format from Upstox.")

        return result


def create_client() -> UpstoxClient:
    """Create an authenticated client using the saved access token."""

    token_data = load_token()

    if token_data is None:
        raise RuntimeError(
            "No saved access token found. Run python get_token.py first."
        )

    return UpstoxClient(token_data["access_token"])

