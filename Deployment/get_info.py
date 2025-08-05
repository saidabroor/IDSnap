import sqlite3

# import psycopg2
# import json

# def connect_db():
#     return psycopg2.connect(
#         dbname="faces",
#         user="postgres",
#         password="aytmiman",
#         host="localhost",
#         port="5432"
#     )


# def get_person_info(id):
#     conn = connect_db()
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM users WHERE id = %s", (id,))
#     row = cur.fetchone()
#     colnames = [desc[0] for desc in cur.description]
#     cur.close()
#     conn.close()
#     return json.dumps(dict(zip(colnames, row)))


# get_person_info(1)

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


# # Test the function
# name = "999"
# info = get_person_info(name)
# print(info)
   