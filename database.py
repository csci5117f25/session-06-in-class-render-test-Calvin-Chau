import psycopg2
import os

DATABASE_URL = 'postgresql://session_06_testing_user:kx1ZBzV1SDfISMhM4ylaVhqlbWZIUgkD@dpg-d38smi1r0fns7388e7k0-a.ohio-postgres.render.com/session_06_testing'
# this should be taken from the .env file

conn = psycopg2.connect(DATABASE_URL)
    
cursor = conn.cursor()

def createTable():
    table = '''
        CREATE TABLE IF NOT EXISTS guestbook (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    message TEXT NOT NULL
    );
    '''
    try:
        cursor.execute(table)
        # commit the transaction so the CREATE TABLE is applied
        conn.commit()
        print("CREATE TABLE executed and committed")
    except Exception as e:
        # rollback on error and re-raise for visibility
        conn.rollback()
        print(f"Error running CREATE TABLE: {e}")
        raise

    
if __name__ == '__main__':
    try:
        createTable()
    finally:
        # ensures the connection is closed even if createTable raises
        cursor.close()
        conn.close()