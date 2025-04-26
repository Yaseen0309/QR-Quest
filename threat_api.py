# threat_api.py
import requests

def check_with_google_safe_browsing(api_key, url_to_check):
    endpoint = "https://safebrowsing.googleapis.com/v4/threatMatches:find"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "client": {
            "clientId": "qr-scam-analyzer",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [
                {"url": url_to_check}
            ]
        }
    }

    response = requests.post(f"{endpoint}?key={api_key}", headers=headers, json=payload)
    result = response.json()
    return bool(result.get("matches"))
