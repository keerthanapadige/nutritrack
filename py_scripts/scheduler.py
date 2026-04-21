import schedule
import time
import logging
from extract import fetch_food_data
from transform import transform_data
from load import insert_data

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Same food configs as load.py
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


def run_pipeline():
    """Runs the full ETL pipeline — extract, transform, load"""
    logging.info("Pipeline started...")

    try:
        all_data = []

        # Step 1 — Extract + Transform
        for config in food_configs:
            logging.info(f"Fetching data for: {config['query']}")

            raw = fetch_food_data(config["query"], page_size=50)

            transformed = transform_data(
                raw,
                required_terms=config["required_terms"],
                excluded_terms=config["excluded_terms"]
            )

            logging.info(f"Transformed {len(transformed)} records for: {config['query']}")
            all_data.extend(transformed)

        # Step 2 — Load
        insert_data(all_data)
        logging.info(f"Pipeline complete! {len(all_data)} total records loaded.")

    except Exception as e:
        logging.error(f"Pipeline failed: {e}")


# Schedule pipeline to run daily at 8:00 AM
schedule.every().day.at("08:00").do(run_pipeline)

if __name__ == "__main__":
    logging.info("Scheduler started! Pipeline runs daily at 08:00 AM")

    # Run once immediately on start
    run_pipeline()

    # Keep scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)