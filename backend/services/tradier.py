import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TRADIER_TOKEN")

BASE_URL = "https://api.tradier.com/v1"  # change to live later

def get_option_chain(symbol: str, expiration: str):
	"""Fetch option chain for a given stock and expiration date."""
	url = f"{BASE_URL}/markets/options/chains"
	headers = {
		"Authorization": f"Bearer {TOKEN}",
		"Accept": "application/json"
	}
	params = {
		"symbol": symbol,
		"expiration": expiration
	}
	response = requests.get(url, headers=headers, params=params)
	if response.status_code == 200:
		return response.json()
	else:
		raise Exception(f"Error {response.status_code}: {response.text}")
