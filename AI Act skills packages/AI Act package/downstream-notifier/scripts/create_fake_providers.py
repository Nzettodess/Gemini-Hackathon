import pandas as pd
from pathlib import Path

def create_provider(filename, data):
    df = pd.DataFrame([data])
    path = Path("examples") / filename
    df.to_excel(path, index=False)
    print(f"Created {path}")

providers = [
    {
        "filename": "Alpha_Provider.xlsx",
        "data": {
            "name": "Alpha Medical AI Solutions",
            "email": "regulator-contact@alpha-med.eu",
            "id": "AI-MED-2026-X1",
            "version": "v3.1.2-LTS",
            "representative": "Dr. Hans Gruber",
            "system_name": "Diagnosys-9000"
        }
    },
    {
        "filename": "Beta_Provider.xlsx",
        "data": {
            "name": "Beta Financial Algorithmic Trading",
            "email": "compliance@beta-fintech.io",
            "id": "FIN-ALGO-BETA",
            "version": "v1.0.0-RC2",
            "representative": "Jean-Luc Picard",
            "system_name": "MarketMaker Pro"
        }
    },
    {
        "filename": "Gamma_Provider.xlsx",
        "data": {
            "name": "Gamma Logistics & Drone Delivery",
            "email": "legal@gamma-logistix.com",
            "id": "LOG-DRONE-G7",
            "version": "v5.5.0",
            "representative": "Ellen Ripley",
            "system_name": "SkyPath Optimizer"
        }
    },
    {
        "filename": "Zenith_Provider.xlsx",
        "data": {
            "name": "Zenith AI Systems Corp",
            "email": "compliance@zenith-ai.com",
            "id": "Z-9000-X",
            "version": "v2.4.0-pro",
            "representative": "Sarah Connor",
            "system_name": "SkyNet Sentinel (LangGraph)"
        }
    }
]

Path("examples").mkdir(exist_ok=True)
for p in providers:
    create_provider(p["filename"], p["data"])
