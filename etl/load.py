def load(students_df, grades_df, engine):
    students_df.to_sql("students", engine, if_exists="append", index=False)
    grades_df.to_sql("grades", engine, if_exists="append", index=False)
    print("[Load] Data successfully pushed to PostgreSQL ✅")