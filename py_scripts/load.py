import psycopg2
import os
from dotenv import load_dotenv
from extract import fetch_food_data
from transform import transform_data

load_dotenv()


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


def insert_data(data):
    conn = get_connection()
    cur = conn.cursor()

    for item in data:
        cur.execute("""
            INSERT INTO food_items (food_name, category)
            VALUES (%s, %s)
            ON CONFLICT (food_name)
            DO UPDATE SET food_name = EXCLUDED.food_name
            RETURNING food_id
        """, (item["food_name"], "general"))

        food_id = cur.fetchone()[0]

        cur.execute("""
            INSERT INTO nutrition_data (
                food_id, calories, protein, carbs, fat, sugar
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (food_id, calories, protein, carbs, fat, sugar)
            DO NOTHING
        """, (
            food_id,
            item["calories"],
            item["protein"],
            item["carbs"],
            item["fat"],
            item["sugar"]
        ))

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    food_configs = [
        {
            "query": "chicken breast",
            "required_terms": ["chicken", "breast"],
            "excluded_terms": ["orange", "curry", "enchilada", "chimichanga", "gravy"]
        },
        {
            "query": "apple raw",
            "required_terms": ["apple"],
            "excluded_terms": ["juice", "pie", "sauce"]
        },
        {
            "query": "egg boiled",
            "required_terms": ["egg"],
            "excluded_terms": ["salad", "sandwich"]
        },
        {
            "query": "rice cooked",
            "required_terms": ["rice"],
            "excluded_terms": ["pudding", "noodles"]
        },
        {
            "query": "whole milk",
            "required_terms": ["milk"],
            "excluded_terms": ["shake", "chocolate", "dessert"]
        }
    ]

    all_data = []

    for config in food_configs:
        raw = fetch_food_data(config["query"], page_size=50)
        transformed = transform_data(
            raw,
            required_terms=config["required_terms"],
            excluded_terms=config["excluded_terms"]
        )
        all_data.extend(transformed)

    insert_data(all_data)

    print("Data loaded into PostgreSQL successfully!")