from flask import Blueprint, request, render_template, redirect, url_for, flash
import psycopg2
from __init__ import db, logger

shoppingcart_bp = Blueprint('shoppingcart', __name__)

@shoppingcart_bp.route('/carts', methods=['GET'])
def get_all_shoppingcarts():
    shoppingcarts = MStore_v1.ShoppingCart.query.all()
    return render_template('shoppingcarts.html', shoppingcarts=shoppingcarts)
#
@shoppingcart_bp.route('/cart/<int:id>', methods=['GET'])
def get_shoppingcart(id):
    shoppingcart = MStore_v1.ShoppingCart.query.get_or_404(id)
    return render_template('shoppingcart_detail.html', shoppingcart=shoppingcart)

@shoppingcart_bp.route('/cart/new', methods=['GET', 'POST'])
def create_shoppingcart():
    if request.method == 'POST':
        data = request.form
        new_shoppingcart = MStore_v1.ShoppingCart(**data)
        db.session.add(new_shoppingcart)
        db.session.commit()
        return redirect(url_for('shoppingcart.get_shoppingcart'))
    return render_template('shoppingcart_form.html', shoppingcart=None)

@shoppingcart_bp.route('/cart/<int:id>/edit', methods=['GET', 'POST'])
def update_shoppingcart(id):
    shoppingcart = MStore_v1.ShoppingCart.query.get_or_404(id)
    if request.method == 'POST':
        data = request.form
        for key, value in data.items():
            setattr(shoppingcart, key, value)
        db.session.commit()
        return redirect(url_for('shoppingcart.get_shoppingcart'))
    return render_template('shoppingcart_form.html', shoppingcart=shoppingcart)

@shoppingcart_bp.route('/cart/<int:id>/delete', methods=['POST'])
def delete_shoppingcart(id):
    shoppingcart = MStore_v1.ShoppingCart.query.get_or_404(id)
    db.session.delete(shoppingcart)
    db.session.commit()
    return redirect(url_for('shoppingcart.get_shoppingcart'))