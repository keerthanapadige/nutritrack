import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FDC_API_KEY")
BASE_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"


def fetch_food_data(query="apple", page_size=50):
    params = {
        "api_key": API_KEY,
        "query": query,
        "pageSize": page_size
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code != 200:
        raise Exception(f"API failed: {response.status_code}")

    return response.json()


if __name__ == "__main__":
    data = fetch_food_data("chicken breast", page_size=50)

    print("Fetched Data Sample:")
    for food in data.get("foods", []):
        print(repr(food.get("description")), "|", repr(food.get("brandName")))