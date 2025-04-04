def store_in_database(resume_data):
    """
    Stores extracted resume information in an SQLite database.
    
    Args:
        resume_data (dict): Extracted structured resume data.
    """
    connection = sqlite3.connect("resumes.db")
    cursor = connection.cursor()

    # Create table if not exists
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_title TEXT,
            skills TEXT,
            experience_years INTEGER,
            education TEXT
        )
    """)

    # Insert extracted data
    cursor.execute("""
        INSERT INTO resumes (job_title, skills, experience_years, education)
        VALUES (?, ?, ?, ?)
    """, (
        resume_data["job_title"],
        ", ".join(resume_data["skills"]),
        resume_data["experience_years"],
        resume_data["education"]
    ))

    connection.commit()
    connection.close()