from flask import Flask, request, render_template_string
import mysql.connector

app = Flask(__name__)

db_config = {
    'host': 'mysql',  # service name in k8s
    'user': 'root',
    'password': 'rootpassword',
    'database': 'itemsdb'
}

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    if request.method == 'POST':
        item = request.form.get('item')
        if item:
            cursor.execute("INSERT INTO items (name) VALUES (%s)", (item,))
            conn.commit()
    cursor.execute("SELECT name FROM items")
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template_string('''
        <h1>Items List</h1>
        <form method="post">
            <input name="item" placeholder="Add item" required>
            <button type="submit">Add</button>
        </form>
        <ul>
            {% for item in items %}
            <li>{{item[0]}}</li>
            {% endfor %}
        </ul>
    ''', items=items)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
