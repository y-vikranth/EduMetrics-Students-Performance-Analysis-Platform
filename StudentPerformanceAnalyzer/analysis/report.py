from analysis.queries import top_students_per_subject, department_averages, at_risk_students

def print_report(engine):
    print("\n📊 Top Students Per Subject:")
    print(top_students_per_subject(engine).to_string(index=False))

    print("\n🏫 Department Averages:")
    print(department_averages(engine).to_string(index=False))

    print("\n⚠️  At-Risk Students (avg < 50):")
    at_risk = at_risk_students(engine)
    if at_risk.empty:
        print("No at-risk students found.")
    else:
        print(at_risk.to_string(index=False))