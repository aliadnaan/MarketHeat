from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
	return {"message": "Welcome to MarketHeat"}

@app.get("/ping")
def ping():
	return {"status": "alive"}
