import sqlite3

def get_person_info(name):
    try:
        # Connect to database
        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()
        
        # Query for information by name
        cursor.execute('SELECT information FROM data WHERE name = ?', (name,))
        result = cursor.fetchone()
        
        # Close connection
        conn.close()
        
        # Return information if found, None if not found
        if result:
            return result[0]
        else:
            return None
            
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None