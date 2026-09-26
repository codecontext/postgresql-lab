CREATE SCHEMA IF NOT EXISTS learning;

CREATE TABLE IF NOT EXISTS learning.students (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    full_name text NOT NULL,
    email text NOT NULL UNIQUE,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS learning.courses (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title text NOT NULL UNIQUE,
    credits integer NOT NULL CHECK (credits > 0)
);

CREATE TABLE IF NOT EXISTS learning.enrollments (
    student_id bigint NOT NULL REFERENCES learning.students (id),
    course_id bigint NOT NULL REFERENCES learning.courses (id),
    enrolled_on date NOT NULL DEFAULT CURRENT_DATE,
    PRIMARY KEY (student_id, course_id)
);

INSERT INTO learning.students (full_name, email)
VALUES
    ('Avery Chen', 'avery.chen@example.test'),
    ('Jordan Rivera', 'jordan.rivera@example.test'),
    ('Morgan Patel', 'morgan.patel@example.test')
ON CONFLICT (email) DO NOTHING;

INSERT INTO learning.courses (title, credits)
VALUES
    ('SQL Fundamentals', 3),
    ('Relational Design', 4),
    ('Query Planning', 3)
ON CONFLICT (title) DO NOTHING;

INSERT INTO learning.enrollments (student_id, course_id)
SELECT students.id, courses.id
FROM learning.students AS students
CROSS JOIN learning.courses AS courses
WHERE (students.email, courses.title) IN (
    ('avery.chen@example.test', 'SQL Fundamentals'),
    ('avery.chen@example.test', 'Relational Design'),
    ('jordan.rivera@example.test', 'SQL Fundamentals'),
    ('morgan.patel@example.test', 'Query Planning')
)
ON CONFLICT (student_id, course_id) DO NOTHING;