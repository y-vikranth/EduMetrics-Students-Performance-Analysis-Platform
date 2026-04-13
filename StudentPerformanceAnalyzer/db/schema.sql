CREATE TABLE IF NOT EXISTS students (
    student_id   SERIAL PRIMARY KEY,
    name         VARCHAR(100),
    age          INT,
    gender       VARCHAR(10),
    department   VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS grades (
    grade_id     SERIAL PRIMARY KEY,
    student_id   INT REFERENCES students(student_id),
    subject      VARCHAR(50),
    score        NUMERIC(5,2),
    semester     VARCHAR(20),
    exam_date    DATE
);