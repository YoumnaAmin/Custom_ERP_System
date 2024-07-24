import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('site.db')
cursor = conn.cursor()

try:
    # Execute SQL command to add date column without NOT NULL constraint
    cursor.execute('ALTER TABLE "order" ADD COLUMN date DATE')

    # Commit the transaction
    conn.commit()
    print("Successfully added 'date' column to 'order' table.")

except sqlite3.Error as e:
    print(f"Error occurred: {e}")

finally:
    # Close the database connection
    conn.close()
