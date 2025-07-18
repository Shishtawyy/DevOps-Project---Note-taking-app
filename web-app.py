from flask import Flask, request, redirect, render_template_string
import pymysql
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='notesuser',
        password='password123',
        db='notesdb',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        note = request.form['note']
        conn = get_db_connection()
        try:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO notes (content) VALUES (%s)", (note,))
                conn.commit()
        finally:
            conn.close()
        return redirect('/')
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT content, created_at FROM notes ORDER BY created_at DESC")
            notes = cur.fetchall()
    finally:
        conn.close()
    
    template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Shishtawy's Note Taking App</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            textarea { width: 100%; padding: 10px; }
            input[type="submit"] { padding: 10px 20px; background: #4CAF50; color: white; border: none; cursor: pointer; }
            .note { border-bottom: 1px solid #ddd; padding: 10px 0; }
            .timestamp { color: #777; font-size: 0.8em; }
        </style>
    </head>
    <body>
        <h1>Shishtawy's Note Taking App</h1>
        <form method="post">
            <textarea name="note" rows="4" placeholder="Write your note here..."></textarea><br><br>
            <input type="submit" value="Save Note">
        </form>
        <h2>Your Notes</h2>
        {% for note in notes %}
        <div class="note">
            <div class="timestamp">🕒 {{ note.created_at }}</div>
            <div>📌 {{ note.content }}</div>
        </div>
        {% endfor %}
    </body>
    </html>
    '''
    return render_template_string(template, notes=notes)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

