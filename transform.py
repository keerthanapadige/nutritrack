from extract import fetch_food_data


def extract_nutrients(nutrients_list):
    nutrient_map = {
        "Energy": "calories",
        "Protein": "protein",
        "Carbohydrate, by difference": "carbs",
        "Total lipid (fat)": "fat",
        "Sugars, total including NLEA": "sugar"
    }

    result = {
        "calories": 0,
        "protein": 0,
        "carbs": 0,
        "fat": 0,
        "sugar": 0
    }

    for nutrient in nutrients_list:
        name = nutrient.get("nutrientName")
        value = nutrient.get("value", 0)

        if name in nutrient_map:
            result[nutrient_map[name]] = value

    return result


def transform_data(raw_data, required_terms=None, excluded_terms=None):
    transformed = []

    required_terms = required_terms or []
    excluded_terms = excluded_terms or []

    for food in raw_data.get("foods", []):
        if food.get("brandOwner"):
            continue

        food_name = food.get("description")

        if not food_name:
            continue

        # Clean and simplify
        food_name = food_name.split(",")[0].strip().title()

        food_name_lower = food_name.lower()

        if required_terms and not all(term in food_name_lower for term in required_terms):
            continue

        if any(term in food_name_lower for term in excluded_terms):
            continue

        nutrients = extract_nutrients(food.get("foodNutrients", []))

        record = {
            "food_name": food_name,
            **nutrients
        }

        transformed.append(record)

    return transformed


if __name__ == "__main__":
    raw_data = fetch_food_data("chicken breast", page_size=50)

    transformed = transform_data(
        raw_data,
        required_terms=["chicken", "breast"],
        excluded_terms=["orange", "curry", "enchilada", "chimichanga", "gravy"]
    )

    print("Transformed Data:")
    for item in transformed:
        print(item)