from db.connection import get_engine, run_schema
from etl.extract import extract
from etl.transform import transform
from etl.load import load
from analysis.report import print_report

def main():
    engine = get_engine()
    run_schema(engine)

    raw_df = extract("data/students.csv")
    students_df, grades_df = transform(raw_df)
    load(students_df, grades_df, engine)

    print_report(engine)

if __name__ == "__main__":
    main()