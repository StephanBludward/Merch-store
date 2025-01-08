from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
import sqlite3
import stripe
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the secret keys
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')

stripe.api_key = STRIPE_SECRET_KEY

app = Flask(__name__)



STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')

stripe.api_key = STRIPE_SECRET_KEY


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
        session['cart'] = []  

# Route to display products
@app.route('/')
def index():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('index.html', products=products)

stripe.api_key = ""  

@app.route('/checkout-session', methods=['POST'])
def create_checkout_session():
    stripe.api_key = STRIPE_SECRET_KEY
    try:
        # Get cart data from the session
        cart = session.get('cart', [])
        if not cart:
            return jsonify({'error': 'Cart is empty!'}), 400

        # Format items for Stripe
        line_items = []
        for item in cart:
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item['name'],
                    },
                    'unit_amount': int(item['price'] * 100),  # Convert dollars to cents
                },
                'quantity': item['quantity'],
            })

        # Create a Stripe Checkout Session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=request.host_url + 'success',  # Redirect after successful payment
            cancel_url=request.host_url + 'cancel',   # Redirect after canceled payment
        )

        return jsonify({'id': checkout_session.id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/success')
def success():
    return render_template('success.html') 

@app.route('/cancel')
def cancel():
    return render_template('cancel.html') 

if __name__ == '__main__':
    app.run(debug=True)
