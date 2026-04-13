# EduMetrics — Student Performance Analytics Platform

A full-stack data engineering and analytics project that simulates a 
real-world academic performance monitoring system. Built with Python, 
PostgreSQL, and Streamlit, it demonstrates an end-to-end data pipeline 
from raw CSV ingestion to an interactive browser-based dashboard.

## 🔍 What This Project Does
- Ingests raw student and grade data from CSV files
- Cleans, validates, and transforms data using Pandas
- Stores structured data in a relational PostgreSQL database
- Runs advanced SQL queries (CTEs, Window Functions, JOINs, HAVING)
- Presents results on a live, interactive Streamlit dashboard with 
  Plotly visualizations

## 🛠️ Tech Stack
| Layer        | Technology                        |
|--------------|-----------------------------------|
| Language     | Python 3.x                        |
| Data         | Pandas                            |
| Database     | PostgreSQL + SQLAlchemy + psycopg2|
| Dashboard    | Streamlit + Plotly                |
| Config       | python-dotenv                     |

## 📊 Dashboard Features
- KPI summary cards (total departments, overall average, at-risk count)
- Department-wise average score bar chart with color scale
- Top 3 students per subject with subject filter dropdown
- At-risk student detection with a live adjustable threshold slider

## 🏗️ Architecture
CSV Data → [Extract] → [Transform] → [Load] → PostgreSQL
                      
↓

Streamlit Dashboard
(Plotly Charts + Tables)

## ⚙️ How to Run
1. Clone this repository
```bash
   git clone https://github.com/your-username/edumetrics.git
   cd edumetrics
```
2. Install dependencies
```bash
   pip install -r requirements.txt
```
3. Set up PostgreSQL and configure `.env`
```env
   DB_USER=your_user
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=student_db
```
4. Run the ETL pipeline
```bash
   python main.py
```
5. Launch the dashboard
```bash
   streamlit run dashboard/app.py
```
   Then open `http://localhost:8501` in your browser.

## 📁 Project Structure

edumetrics/

├── data/ # Raw CSV input

├── db/                 # DB connection & schema

├── etl/                # Extract, Transform, Load pipeline

├── analysis/           # SQL queries & reporting logic

├── dashboard/          # Streamlit app

└── main.py             # ETL entry point

## 💡 Key Concepts Demonstrated
- ETL pipeline design
- Relational database schema design (foreign keys, normalization)
- Advanced SQL (CTEs, Window Functions, GROUP BY, HAVING)
- Data cleaning and transformation with Pandas
- Interactive data visualization with Plotly
- Modular, production-style Python project structure