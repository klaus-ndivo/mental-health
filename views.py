from datetime import datetime
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from . import db
from .models import OrderItem, Product, Order, OrderDetails
from .forms import OrderForm

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('home.html')

@main.route('/home')
def home():
    return render_template('home.html', active_page='home')

@main.route('/clothing')
def clothing():
    return render_template('clothing.html', active_page='clothing')

@main.route('/accessories')
def accessories():
    return render_template('accessories.html', active_page='accessories')

@main.route('/cart', methods=['GET'])
def cart():
    form = OrderForm()
    return render_template('cart.html', form=form)

@main.route('/contentDetails')
def contentDetails():
    return render_template('contentDetails.html')

@main.route('/orderPlaced')
def orderPlaced():
    return render_template('orderPlaced.html')

@main.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').strip().lower()
    return render_template('search.html', query=query)

@main.route('/submit_order', methods=['POST'])
def submit_order():
    form = OrderForm(request.form)
    if form.validate():
        # Process the order
        name = form.name.data
        email = form.email.data
        address = form.address.data
        # Create a new order
        order = Order(order_date=datetime.now())
        db.session.add(order)
        db.session.commit()
        
         # Retrieve items from the cart
        cart_items = request.cookies.get('orderId', '').split(' ')
        for item_id in cart_items:
            if item_id:
                product = Product.query.get(item_id)
                if product:
                    quantity = cart_items.count(item_id)
                    total_price = (product.price * quantity)/100
                        
                        # Create an order item and associate it with the order
                    order_item = OrderItem(order=order, product_id=product.id, quantity=quantity, total_price=total_price)
                    orderDetails = OrderDetails(order=order, product_id = product.id, name=name, email=email, address=address)
                    db.session.add(order_item)
                    db.session.add(orderDetails)
            
        db.session.commit()
        return jsonify(success=True)
    return jsonify(success=False, errors=form.errors)


@main.route('/save-product', methods=['POST'])
def save_product():
    product_data = request.json.get('product')
    category = request.json.get('category')

    if product_data and category:
        existing_product = Product.query.filter_by(id=product_data['id']).first()
        if existing_product:
            return "Product already exists", 200

        product = Product(
            id=product_data['id'],
            name=product_data['name'],
            price=product_data['price'],
            description=product_data['description'],
            category=category
        )
        db.session.add(product)
        db.session.commit()
        return "Product saved successfully", 201
    else:
        return "Invalid request data", 400