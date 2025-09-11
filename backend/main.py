from fastapi import FastAPI
import random
from services.tradier import get_option_chain

app = FastAPI()

@app.get("/")
def root():
	return {"message": "Welcome to MarketHeat 🔥"}

@app.get("/ping")
def ping():
	return {"status": "alive"}

# ---------------------------
# DUMMY ALERTS (kept for testing)
# ---------------------------
@app.get("/dummy")
def dummy():
	alerts = []
	for _ in range(5):
		volume = random.randint(50, 5000)
		open_interest = random.randint(10, 4000)
		premium_value = random.randint(50_000, 1_000_000)

		trade = {
			"symbol": random.choice(["AAPL", "TSLA", "NVDA", "AMZN"]),
			"strike": round(random.uniform(50, 500), 2),
			"type": random.choice(["CALL", "PUT"]),
			"premium": f"${premium_value:,}",
			"volume": volume,
			"open_interest": open_interest,
			"is_whale": False
		}

		if volume > open_interest or premium_value > 100_000:
			trade["is_whale"] = True

		alerts.append(trade)

	return {"alerts": alerts}

# ---------------------------
# REAL ALERTS (Tradier data)
# ---------------------------
@app.get("/alerts")
def alerts(symbol: str, expiration: str):
    """Fetch option chain from Tradier and return only whale trades."""
    data = get_option_chain(symbol, expiration)

    option_chain = data.get("options", {}).get("option", [])

    alerts = []
    for opt in option_chain:
        volume = opt.get("volume") or 0
        open_interest = opt.get("open_interest") or 0
        bid = opt.get("bid") or 0.0
        ask = opt.get("ask") or 0.0
        last = opt.get("last") or 0.0

        # Compute mid price safely
        if bid > 0 and ask > 0:
            mid_price = (bid + ask) / 2
        else:
            mid_price = last

        # Compute premium safely
        premium_value = (mid_price or 0) * (volume or 0) * 100

        # Whale rule check
        if premium_value > 100_000:
            trade = {
                "symbol": symbol,
                "expiration": expiration,
                "strike": opt.get("strike"),
                "type": opt.get("option_type"),
                "volume": volume,
                "open_interest": open_interest,
                "premium": f"${premium_value:,.0f}"
            }
            alerts.append(trade)

    return {"alerts": alerts}


