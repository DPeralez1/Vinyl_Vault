import os

from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Access to SQLite database
db_path = os.path.join(os.getcwd(), "vinyl_records.db")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        # Add user input to database
        name = request.form.get('artist_name')
        if not name:
            return redirect('/')

        album = request.form.get('album_name')
        if not album:
            return redirect('/')

        # Connect to the SQLite database
        # Using with ensures that the connection is properly closed after the block of code is executed
        with sqlite3.connect(db_path) as conn:

            # The cursor object allows you to execute SQL commands.
            cursor = conn.cursor()

            # Insert user input into the database
            cursor.execute("INSERT INTO vinyl_records (artist_name, album_name) VALUES (?, ?)", (name, album))

            # This commits the transaction to the database, saving any changes made.
            conn.commit()

        return redirect('/')
    else:
     # Display all records, sorted by artist name
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM vinyl_records ORDER BY artist_name ASC")
            vinyl_records = cursor.fetchall()
        return render_template('index.html', vinyl_records=vinyl_records)


@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        # Delete the record from the database
        cursor.execute("DELETE FROM vinyl_records WHERE id = ?", (id,))
        conn.commit()

    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)
