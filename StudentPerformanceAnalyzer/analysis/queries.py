import pandas as pd

def top_students_per_subject(engine):
    query = """
        WITH ranked AS (
            SELECT s.name, g.subject, g.score,
                   RANK() OVER (PARTITION BY g.subject ORDER BY g.score DESC) AS rnk
            FROM grades g
            JOIN students s ON g.student_id = s.student_id
        )
        SELECT * FROM ranked WHERE rnk <= 3;
    """
    return pd.read_sql(query, engine)

def department_averages(engine):
    query = """
        SELECT s.department,
               ROUND(AVG(g.score), 2) AS avg_score,
               COUNT(DISTINCT s.student_id) AS num_students
        FROM grades g
        JOIN students s ON g.student_id = s.student_id
        GROUP BY s.department
        ORDER BY avg_score DESC;
    """
    return pd.read_sql(query, engine)

def at_risk_students(engine, threshold=50):
    query = f"""
        SELECT s.name, s.department, ROUND(AVG(g.score), 2) AS avg_score
        FROM grades g
        JOIN students s ON g.student_id = s.student_id
        GROUP BY s.student_id, s.name, s.department
        HAVING AVG(g.score) < {threshold}
        ORDER BY avg_score ASC;
    """
    return pd.read_sql(query, engine)