from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json, statistics, os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

DATA_PATH = os.path.join(os.path.dirname(__file__), "telemetry.json")

with open(DATA_PATH) as f:
    data = json.load(f)

@app.post("/api/latency")
async def latency(payload: dict):
    regions = payload["regions"]
    threshold = payload["threshold_ms"]
    result = {}

    for region in regions:
        records = [r for r in data if r["region"] == region]
        lats = [r["latency_ms"] for r in records]
        ups = [r["uptime"] for r in records]

        result[region] = {
            "avg_latency": sum(lats)/len(lats),
            "p95_latency": sorted(lats)[int(0.95*len(lats))-1],
            "avg_uptime": sum(ups)/len(ups),
            "breaches": sum(1 for x in lats if x > threshold)
        }

    return result
