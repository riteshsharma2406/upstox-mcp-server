import json
import os
import secrets
import threading
import time
import webbrowser
import httpx

from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlencode, urlparse, parse_qs
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('UPSTOX_API_KEY')
API_SECRET = os.getenv('UPSTOX_API_SECRET')
REDIRECT_URL = os.getenv('UPSTOX_REDIRECT_URL')
AUTH_URL = "https://api.upstox.com/v2/login/authorization/dialog"
TOKEN_URL = "https://api.upstox.com/v2/login/authorization/token"

TOKEN_FILE = Path(__file__).resolve().parent / "upstox_token.json"
CALLBACK_TIMEOUT_SECONDS = 180

def validate_config() -> None:
    """Validate required Upstox OAuth configuration without exposing secrets."""

    missing = []

    if not API_KEY or API_KEY == "your_upstox_api_key":
        missing.append("UPSTOX_API_KEY")

    if not API_SECRET or API_SECRET == "your_upstox_api_secret":
        missing.append("UPSTOX_API_SECRET")

    if not REDIRECT_URL:
        missing.append("UPSTOX_REDIRECT_URL")

    if missing:
        raise ValueError(
            "Missing or placeholder configuration values: "
            + ", ".join(missing)
            + ". Update your local .env file."
        )

    parsed = urlparse(REDIRECT_URL)

    if (
        parsed.scheme != "http"
        or parsed.hostname not in {"localhost", "127.0.0.1"}
        or parsed.port != 3000
        or parsed.path != "/callback"
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError(
            "UPSTOX_REDIRECT_URL must be "
            "http://localhost:3000/callback "
            "or http://127.0.0.1:3000/callback."
        )

class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """Handle the local callback from Upstox OAuth authorization."""

    expected_state = None
    authorization_code = None
    authorization_error = None

    def do_GET(self):
        """Validate the callback and capture the authorization code."""

        parsed_url = urlparse(self.path)

        if parsed_url.path != "/callback":
            self.send_error(404, "Not found")
            return

        query_params = parse_qs(parsed_url.query)

        returned_state = query_params.get("state", [None])[0] #it return list containing state so [0] to access the list

        if (
            not self.expected_state
            or not returned_state
            or not secrets.compare_digest(
                returned_state,
                self.expected_state,
            )
        ):
            self.send_error(400, "Invalid OAuth state")
            return

        error = query_params.get("error", [None])[0]

        if error:
            type(self).authorization_error = error
            response_message = (
                "Upstox authorization was unsuccessful. "
                "You may close this browser window."
            )

            self.send_response(400)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(response_message.encode("utf-8"))
            return

        code = query_params.get("code", [None])[0]

        if not code:
            self.send_error(400, "Authorization code missing")
            return

        type(self).authorization_code = code

        response_message = (
            "Upstox authorization received successfully. "
            "You may close this browser window."
        )

        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(response_message.encode("utf-8"))

    def log_message(self, format, *args):
        """Suppress default HTTP logs that could expose callback details."""
        return

def build_authorization_url(state: str) -> str:

    validate_config()

    params = {
        "client_id":API_KEY,
        "redirect_uri": REDIRECT_URL,
        "response_type": "code",
        "state": state
    }

    return f"{AUTH_URL}?{urlencode(params)}"

def generate_state() -> str:
    return secrets.token_urlsafe(32)

def prepare_authorization() -> str:
    state = generate_state()
    OAuthCallbackHandler.expected_state = state
    OAuthCallbackHandler.authorization_code = None
    OAuthCallbackHandler.authorization_error = None
    authorization_url = build_authorization_url(state)
    return authorization_url

def exchange_authorization_code(code: str) -> dict:

    validate_config()

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "code": code,
        "client_id": API_KEY,
        "client_secret": API_SECRET,
        "redirect_uri": REDIRECT_URL,
        "grant_type": "authorization_code",
    }

    try:
        response = httpx.post(
            TOKEN_URL,
            headers=headers,
            data=data,
            timeout=20.0,
        )

        response.raise_for_status()

    except httpx.HTTPStatusError as exc:
        raise RuntimeError(
            f"Upstox token exchange failed with HTTP status "
            f"{exc.response.status_code}."
        ) from None

    except httpx.RequestError:
        raise RuntimeError(
            "Could not connect to Upstox. Check your internet connection."
        ) from None

    try:
        token_data = response.json()
    except ValueError:
        raise RuntimeError(
            "Upstox returned an invalid JSON response."
        ) from None

    if not isinstance(token_data, dict) or not token_data.get("access_token"):
        raise RuntimeError(
            "Upstox response did not contain an access token."
        )

    return token_data

def save_token(token_data: dict) -> None:
    if not isinstance(token_data, dict) or not token_data.get("access_token"):
        raise ValueError("Cannot save token: access token is missing.")

    temporary_file = TOKEN_FILE.with_suffix(".tmp")

    try:
        with temporary_file.open("w", encoding="utf-8") as file:
            json.dump(token_data, file, indent=2)

        temporary_file.replace(TOKEN_FILE)

    finally:
        if temporary_file.exists():
            temporary_file.unlink()

def load_token() -> dict | None:
    if not TOKEN_FILE.exists():
        return None

    try:
        with TOKEN_FILE.open("r", encoding="utf-8") as file:
            token_data = json.load(file)
    except (OSError, json.JSONDecodeError):
        return None

    if not isinstance(token_data, dict):
        return None

    if not token_data.get("access_token"):
        return None

    return token_data

def main() -> None:
    server = None

    try:
        validate_config()

        authorization_url = prepare_authorization()

        server = start_callback_server()

        print("Opening Upstox authorization page...")
        webbrowser.open(authorization_url)

        print("Waiting for Upstox authorization...")

        deadline = time.monotonic() + CALLBACK_TIMEOUT_SECONDS

        while (
            OAuthCallbackHandler.authorization_code is None
            and OAuthCallbackHandler.authorization_error is None
            and time.monotonic() < deadline
        ):
            time.sleep(0.2)

        if OAuthCallbackHandler.authorization_error:
            raise RuntimeError("Upstox authorization was unsuccessful.")

        code = OAuthCallbackHandler.authorization_code

        if not code:
            raise TimeoutError(
                "Authorization timed out. Please run the script again."
            )

        token_data = exchange_authorization_code(code)

        save_token(token_data)

        print("Upstox access token saved successfully.")

    finally:
        if server is not None:
            server.shutdown()
            server.server_close()

def start_callback_server() -> HTTPServer:
    server = HTTPServer(
        ("127.0.0.1", 3000),
        OAuthCallbackHandler,
    )
    server_thread = threading.Thread(
        target=server.serve_forever,
        daemon=True,
    )
    server_thread.start()
    return server

if __name__ == "__main__":
    main()