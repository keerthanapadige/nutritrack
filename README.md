# NutriTrack 🥗

A Python-based ETL data pipeline that fetches real nutrition data from the **USDA FoodData Central API**, cleans and transforms it, stores it in **PostgreSQL**, and generates nutrition insights.

---

## 📁 Project Structure

```
nutritrack/
├── py_scripts/
│   ├── extract.py          → fetches raw food data from USDA API
│   ├── transform.py        → cleans, filters and maps nutrition data
│   ├── load.py             → loads transformed data into PostgreSQL
│   ├── ai_insights.py      → generates nutrition insights from database
│   └── scheduler.py        → automates full pipeline daily at 08:00 AM
├── data/
│   └── schema.sql          → PostgreSQL database schema
├── queries/
│   └── food_nutrition.sql  → analytical SQL queries
├── dashboard/              → (coming soon)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ How the Pipeline Works

```
USDA FoodData Central API
          ↓
     extract.py        → fetches raw food + nutrient data
          ↓
     transform.py      → filters branded foods out
                         cleans food names
                         maps nutrients to clean columns
          ↓
     load.py           → inserts records into PostgreSQL
          ↓
     ai_insights.py    → runs insights on stored data
          ↓
     scheduler.py      → automates full pipeline daily
```

---

## 🔄 Nutrients Tracked

| USDA Nutrient Name                  | Column   |
|-------------------------------------|----------|
| Energy                              | calories |
| Protein                             | protein  |
| Carbohydrate, by difference         | carbs    |
| Total lipid (fat)                   | fat      |
| Sugars, total including NLEA        | sugar    |

---

## 📊 AI Insights

Running `ai_insights.py` generates:
- 🔥 Highest calorie food
- 💪 Highest protein food
- 🍬 Lowest sugar food
- 📊 Average nutrients across all foods
- 🏆 Top 5 high protein foods

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | ETL pipeline |
| USDA FoodData Central API | Nutrition data source |
| PostgreSQL | Data storage |
| psycopg2 | PostgreSQL connector |
| schedule | Pipeline automation |
| python-dotenv | Environment variables |

---

## 🚀 How to Run

### 1. Clone the repo
```bash
git clone https://github.com/yourname/nutritrack.git
cd nutritrack
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup environment variables
Create a `.env` file in root:
```
FDC_API_KEY=your_usda_api_key
DB_HOST=localhost
DB_NAME=nutritrack
DB_USER=your_db_user
DB_PASSWORD=your_db_password
```

### 5. Run pipeline manually
```bash
python py_scripts/extract.py
python py_scripts/load.py
python py_scripts/ai_insights.py
```

### 6. Run automated scheduler
```bash
python py_scripts/scheduler.py
```

---

## 🔑 Get USDA API Key

1. Go to https://fdc.nal.usda.gov/api-guide.html
2. Sign up for a free API key
3. Add it to your `.env` file as `FDC_API_KEY`

---

## 📝 SQL Queries

Located in `queries/food_nutrition.sql`:
- Top 2 foods by calories using DENSE_RANK()
- Average nutrition per food category
- Protein to calorie ratio analysis
