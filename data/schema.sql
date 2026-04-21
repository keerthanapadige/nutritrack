CREATE TABLE food_items (
    food_id SERIAL PRIMARY KEY,
    food_name TEXT NOT NULL,
    category TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE nutrition_data (
    nutrition_id SERIAL PRIMARY KEY,
    food_id INT REFERENCES food_items(food_id),
    calories FLOAT,
    protein FLOAT,
    carbs FLOAT,
    fat FLOAT,
    sugar FLOAT,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE food_items
ADD CONSTRAINT unique_food_name UNIQUE (food_name);