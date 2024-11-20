from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
import sqlite3

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'  # Use filesystem for session storage
Session(app)

def get_db_connection():
    conn = sqlite3.connect("products.db")  
    conn.row_factory = sqlite3.Row     
    return conn

@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    product_id = request.json.get('id')
    name = request.json.get('name')
    price = request.json.get('price')

    # Check if the item already exists in the cart
    for item in session['cart']:
        if item['id'] == product_id:
            item['quantity'] += 1
            session.modified = True
            return jsonify(session['cart'])

    # If the item is new, add it to the cart
    session['cart'].append({
        'id': product_id,
        'name': name,
        'price': price,
        'quantity': 1
    })
    session.modified = True
    return jsonify(session['cart'])


@app.route('/cart')
def cart():
    return render_template('cart.html', cart=session['cart'])

@app.route('/remove-from-cart', methods=['POST'])
def remove_from_cart():
    product_id = request.json.get('id')

    # Filter the session cart to exclude the removed item
    session['cart'] = [item for item in session['cart'] if item['id'] != product_id]
    session.modified = True
    return jsonify(session['cart'])


@app.before_request
def init_cart():
    if 'cart' not in session:
        session['cart'] = []  # Cart will store a list of items

# Route to display products
@app.route('/')
def index():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('index.html', products=products)


if __name__ == '__main__':
    app.run(debug=True)
