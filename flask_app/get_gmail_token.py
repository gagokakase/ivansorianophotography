"""One-time script to get a Gmail OAuth2 refresh token.

Usage:
  1. Set GMAIL_OAUTH_CLIENT_ID and GMAIL_OAUTH_CLIENT_SECRET in .env
  2. Run: python get_gmail_token.py
  3. Open the printed URL in your browser
  4. Authorize and copy the code from the redirect URL
  5. Run: python get_gmail_token.py PASTE_CODE_HERE
  6. Add the refresh token to .env as GMAIL_OAUTH_REFRESH_TOKEN
"""

import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.environ.get("GMAIL_OAUTH_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("GMAIL_OAUTH_CLIENT_SECRET", "")
REDIRECT_URI = "http://localhost:8080"
SCOPE = "https://www.googleapis.com/auth/gmail.send"

if not CLIENT_ID or not CLIENT_SECRET:
    print("ERROR: Set GMAIL_OAUTH_CLIENT_ID and GMAIL_OAUTH_CLIENT_SECRET in .env first.")
    exit(1)

if len(sys.argv) < 2:
    auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope={SCOPE}"
        f"&access_type=offline"
        f"&prompt=consent"
    )
    print("\n1. Open this URL in your browser:\n")
    print(auth_url)
    print("\n2. After authorizing, you'll be redirected to localhost:8080")
    print("   The page won't load - that's fine. Copy the 'code' parameter from the URL.")
    print("\n3. Run: python get_gmail_token.py PASTE_CODE_HERE\n")
    exit(0)

code = sys.argv[1]

resp = requests.post(
    "https://oauth2.googleapis.com/token",
    data={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
    },
    timeout=15,
)

if resp.status_code == 200:
    data = resp.json()
    refresh_token = data.get("refresh_token", "")
    print(f"\nSUCCESS! Add this to your .env and Railway variables:")
    print(f"GMAIL_OAUTH_REFRESH_TOKEN={refresh_token}")
else:
    print(f"\nERROR: {resp.status_code} - {resp.text}")
