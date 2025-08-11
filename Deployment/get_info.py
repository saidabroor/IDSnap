import sqlite3

def get_person_info(name):
    try:
        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()

        # Make the query case-insensitive
        cursor.execute(
            'SELECT information FROM data WHERE LOWER(name) = ?',
            (name.strip().lower(),)
        )
        result = cursor.fetchone()
        conn.close()

        return result[0] if result else None

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
