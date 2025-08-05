import sqlite3

# Connect to database (creates if doesn't exist)
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS data (
        name TEXT,
        information TEXT
    )
''')

# Example: Insert some sample data
sample_data = [
    ('996', '996 is passionate about artificial intelligence research. He spends hours studying neural networks and machine learning algorithms. In his free time, he enjoys hiking in the mountains. He also volunteers at a local coding bootcamp to teach kids programming. Recently, he started experimenting with building AI-powered chatbots.'),
    ('997', '997 is an avid chess player who competes in local tournaments. He has a vast collection of historical strategy books. Every morning, he practices yoga to stay focused. He works as a freelance graphic designer and loves creating digital art. On weekends, he teaches chess to beginners at the community center.'),
    ('998', '998 is a skilled carpenter who builds custom furniture. He finds inspiration in nature and often incorporates organic shapes into his designs. He enjoys cycling and explores new trails every weekend. He’s also learning to play the violin to challenge himself creatively. At night, he reads science fiction novels to unwind.'),
    ('999', '999 is a professional baker known for his intricate cake designs. He loves experimenting with exotic flavors like saffron and matcha. He’s an early riser and jogs daily to clear his mind. He dreams of opening his own patisserie someday. He also mentors young bakers at a local culinary school.'),
    ('1000', '1000 is a wildlife photographer who travels to remote locations. He’s dedicated to raising awareness about endangered species through his work. He enjoys kayaking on calm rivers to relax. He’s learning to speak French to connect with international conservation groups. At home, he grows rare orchids as a hobby.'),
    ('saidabror', 'This is me. AI Engineer, Inha graduate, MMA fighter'),
    ('ulugbek', 'This is Ulugbek Kadirov. Uzbek actor, Boxer and singer.')
]



cursor.executemany('INSERT INTO data VALUES (?, ?)', sample_data)

# Commit changes and close connection
conn.commit()
conn.close()

print("Database created and sample data inserted successfully!")