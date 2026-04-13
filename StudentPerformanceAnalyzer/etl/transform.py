import pandas as pd

def transform(df: pd.DataFrame):
    df = df.drop_duplicates().dropna()

    df["name"] = df["name"].str.strip().str.title()
    df["subject"] = df["subject"].str.strip().str.title()
    df["department"] = df["department"].str.strip().str.upper()

    df["grade_letter"] = pd.cut(
        df["score"],
        bins=[0, 40, 55, 70, 85, 100],
        labels=["F", "D", "C", "B", "A"]
    )

    students_df = df[["student_id", "name", "age", "gender", "department"]].drop_duplicates()
    grades_df = df[["student_id", "subject", "score", "semester", "exam_date"]]

    print(f"[Transform] {len(students_df)} students, {len(grades_df)} grade records")
    return students_df, grades_df
