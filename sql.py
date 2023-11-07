import sqlite3

# Path to your SQLite database file
db_path = 'translations.db'

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except sqlite3.Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def create_table():
    """ create a table in the SQLite database """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS translations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL,
            language TEXT NOT NULL,
            translation TEXT NOT NULL
        );
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

import sqlite3

class Translation:
    db_path = 'translations.db'  # Path to your SQLite database file
    
    def __init__(self, word, language, translation):
        self.word = word
        self.language = language
        self.translation = translation
    
    def save(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO translations (word, language, translation) 
            VALUES (?, ?, ?)
        ''', (self.word, self.language, self.translation))
        conn.commit()
        inserted_id = cursor.lastrowid
        conn.close()
        return inserted_id
    
    @staticmethod
    def find(word, language):
        conn = sqlite3.connect(Translation.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM translations
            WHERE word = ? AND language = ?
        ''', (word, language))
        translation = cursor.fetchone()
        conn.close()
        return translation
    
    @staticmethod
    def update(word, language, new_translation):
        conn = sqlite3.connect(Translation.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE translations
            SET translation = ?
            WHERE word = ? AND language = ?
        ''', (new_translation, word, language))
        conn.commit()
        conn.close()
    
    @staticmethod
    def delete(word, language):
        conn = sqlite3.connect(Translation.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM translations
            WHERE word = ? AND language = ?
        ''', (word, language))
        conn.commit()
        conn.close()

if __name__ == '__main__':    
    # First, ensure the connection to the db can be established
    create_connection(db_path)

    # Then, create the table
    create_table()
