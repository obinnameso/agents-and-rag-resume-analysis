import psycopg2

# PostgreSQL configuration
DB_CONFIG = {
    "dbname": "resumes_db",
    "user": "postgres",
    "password": "",
    "host": "localhost",
    "port": 5432
}

def store_resume_to_postgres(data):
    """
    Stores extracted resume data to PostgreSQL.
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resumes (
                id SERIAL PRIMARY KEY,
                job_title TEXT,
                skills TEXT,
                experience_years INTEGER,
                education TEXT
            );
        """)

        cursor.execute("""
            INSERT INTO resumes (job_title, skills, experience_years, education)
            VALUES (%s, %s, %s, %s);
        """, (
            data["job_title"],
            ", ".join(data["skills"]),
            data["experience_years"],
            data["education"]
        ))

        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Resume info saved to PostgreSQL.")
    except Exception as e:
        print("❌ Failed to store to database:", e)
