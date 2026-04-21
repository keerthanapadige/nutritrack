import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


def get_all_foods():
    """Fetch all food records from database"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT f.food_name, n.calories, n.protein, n.carbs, n.fat, n.sugar
        FROM food_items f
        JOIN nutrition_data n ON f.food_id = n.food_id
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return rows


def highest_calories():
    """Find food with highest calories"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT f.food_name, n.calories
        FROM food_items f
        JOIN nutrition_data n ON f.food_id = n.food_id
        ORDER BY n.calories DESC
        LIMIT 1
    """)

    result = cur.fetchone()
    cur.close()
    conn.close()

    print(f"Highest Calorie Food: {result[0]} → {result[1]} kcal")


def highest_protein():
    """Find food with highest protein"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT f.food_name, n.protein
        FROM food_items f
        JOIN nutrition_data n ON f.food_id = n.food_id
        ORDER BY n.protein DESC
        LIMIT 1
    """)

    result = cur.fetchone()
    cur.close()
    conn.close()

    print(f"Highest Protein Food: {result[0]} → {result[1]}g")


def lowest_sugar():
    """Find food with lowest sugar"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT f.food_name, n.sugar
        FROM food_items f
        JOIN nutrition_data n ON f.food_id = n.food_id
        ORDER BY n.sugar ASC
        LIMIT 1
    """)

    result = cur.fetchone()
    cur.close()
    conn.close()

    print(f"Lowest Sugar Food: {result[0]} → {result[1]}g")


def avg_nutrients():
    """Show average nutrients across all foods"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            ROUND(AVG(calories)::numeric, 2) AS avg_calories,
            ROUND(AVG(protein)::numeric, 2)  AS avg_protein,
            ROUND(AVG(carbs)::numeric, 2)    AS avg_carbs,
            ROUND(AVG(fat)::numeric, 2)      AS avg_fat,
            ROUND(AVG(sugar)::numeric, 2)    AS avg_sugar
        FROM nutrition_data
    """)

    result = cur.fetchone()
    cur.close()
    conn.close()

    print("\n📊 Average Nutrients Across All Foods:")
    print(f"  Calories : {result[0]} kcal")
    print(f"  Protein  : {result[1]}g")
    print(f"  Carbs    : {result[2]}g")
    print(f"  Fat      : {result[3]}g")
    print(f"  Sugar    : {result[4]}g")


def top_5_protein_foods():
    """Top 5 high protein foods"""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT f.food_name, n.protein, n.calories
        FROM food_items f
        JOIN nutrition_data n ON f.food_id = n.food_id
        ORDER BY n.protein DESC
        LIMIT 5
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    print("\n💪 Top 5 High Protein Foods:")
    for i, row in enumerate(rows, 1):
        print(f"  {i}. {row[0]} → Protein: {row[1]}g | Calories: {row[2]} kcal")


if __name__ == "__main__":
    print("=" * 50)
    print("       🥗 NutriTrack AI Insights")
    print("=" * 50)

    highest_calories()
    highest_protein()
    lowest_sugar()
    avg_nutrients()
    top_5_protein_foods()

    print("\n" + "=" * 50)