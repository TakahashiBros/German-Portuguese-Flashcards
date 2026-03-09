import sqlite3

def create_connection():
    # This creates a connection to a database file. 
    # If 'flashcards.db' doesn't exist, SQLite automatically creates it for you.
    conn = sqlite3.connect('flashcards.db')
    return conn

def setup_database():
    conn = create_connection()
    cursor = conn.cursor()
    
    # Write the SQL command to create our table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            german_word TEXT UNIQUE NOT NULL,
            portuguese_translation TEXT NOT NULL,
            german_definition TEXT,
            review_score INTEGER DEFAULT 0
        )
    ''')
    
    # Save the changes and close the connection
    conn.commit()
    conn.close()
    print("Database is set up and ready to go!")

def add_word(german, portuguese, definition):
    conn = create_connection()
    cursor = conn.cursor()
    
    try:
        # The question marks (?, ?, ?) are placeholders. This is a security 
        # best practice to prevent "SQL Injection" attacks.
        cursor.execute('''
            INSERT INTO words (german_word, portuguese_translation, german_definition)
            VALUES (?, ?, ?)
        ''', (german, portuguese, definition))
        
        conn.commit()
        print(f"Success! Added '{german}' to your flashcards.")
        
    except sqlite3.IntegrityError:
        # This catches the error if you try to add a word that already exists
        print(f"Note: '{german}' is already in your database.")
        
    finally:
        conn.close()

def reset_database():
    conn = create_connection()
    cursor = conn.cursor()
    
    # DROP TABLE completely destroys the table and all its data
    cursor.execute('DROP TABLE IF EXISTS words')
    
    conn.commit()
    conn.close()
    
    # Immediately rebuild the empty table
    setup_database()
    print("Database has been completely wiped and reset!")

def get_all_words_shuffled():
    conn = create_connection()
    cursor = conn.cursor()
    
    # Notice we removed "LIMIT 1". We want ALL the rows, just shuffled!
    cursor.execute('''
        SELECT german_word, portuguese_translation, german_definition 
        FROM words 
        ORDER BY RANDOM() 
    ''')
    
    # fetchall() grabs every single row and puts them into a Python list
    deck = cursor.fetchall() 
    conn.close()
    
    return deck

def get_all_words():
    """Returns a list of all German words in alphabetical order."""
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT german_word FROM words ORDER BY german_word ASC')
    # This takes the rows and flattens them into a simple Python list
    words = [row[0] for row in cursor.fetchall()] 
    conn.close()
    
    return words

def delete_word(german_word):
    """Deletes a specific word from the database."""
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM words WHERE german_word = ?', (german_word,))
    
    conn.commit()
    conn.close()

def reset_database():
    """Completely wipes the database table and recreates it."""
    conn = create_connection()
    cursor = conn.cursor()
    
    cursor.execute('DROP TABLE IF EXISTS words')
    
    conn.commit()
    conn.close()
    
    # Rebuild the empty structure immediately
    setup_database()
    
# This runs the setup automatically if you execute this file directly
if __name__ == "__main__":
    setup_database()