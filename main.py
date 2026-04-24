import os
import uuid
import psycopg2
from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

def get_db_connection():
    # Railway automatically provides the DATABASE_URL environment variable
    return psycopg2.connect(os.environ["DATABASE_URL"])

@app.get("/database", response_class=HTMLResponse)
def database():
    # Print statement for the application logs
    print("Print statement inside the Python database() method. Chris Hastings", flush=True)

    conn = get_db_connection()
    cur = conn.cursor()
    
    # 1. Create table
    cur.execute("CREATE TABLE IF NOT EXISTS table_timestamp_and_random_string (tick timestamp, random_string varchar(50))")
    
    # 2. Generate random string and insert
    random_str = str(uuid.uuid4())[:8]
    cur.execute("INSERT INTO table_timestamp_and_random_string (tick, random_string) VALUES (%s, %s)", (datetime.now(), random_str))
    conn.commit()
    
    # 3. Retrieve all records
    cur.execute("SELECT * FROM table_timestamp_and_random_string")
    rows = cur.fetchall()
    
    cur.close()
    conn.close()
    
    # 4. Format HTML output
    html_content = "<h1>Python/FastAPI Database Output</h1><ul>"
    for row in rows:
        html_content += f"<li>Read from DB: {row[0]} {row[1]}</li>"
    html_content += "</ul>"
    
    return html_content