import json
from pathlib import Path
from typing import List,Dict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_FILE = BASE_DIR / "data" / "products.json"

print(DATA_FILE)

def load_products() -> List[Dict]:
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE,"r",encoding="utf-8") as file:
        return json.load(file)


def get_all_product() -> List[Dict]:
    return load_products()