from flask import Blueprint, request, render_template, redirect, url_for, flash
import psycopg2
import bcrypt
from __init__ import db, logger

managerregist_bp = Blueprint('register_manager', __name__)

@managerregist_bp.route('/register_manager', methods=['GET', 'POST'])
def register_manager():
    if request.method == 'POST':
        storeManagerName = request.form['storeManagerName']
        storeManagerPssw = request.form['storeManagerPssw']
        storeName = request.form['storeName']
        storeTaxId = request.form['storeTaxId']
        storePhone = request.form['storePhone']
        storeEmail = request.form['storeEmail']
        storeAddress = request.form['storeAddress']
        storeLogoUrl = request.form.get('storeLogoUrl')
        storeManager_id = request.form['storeManager_id']

        #hashed_passw = bcrypt.hashpw(storeManagerPssw.encode('utf-8'), bcrypt.gensalt())
        #storeManagerPssw  = hashed_passw

        conn = db.engine.raw_connect
        cur = conn.cursor()
        logger.debug('db connected')

        try:
            cur.execute("""
                INSERT INTO Store (storeManagerName, storeManagerPssw, storeName, storeTaxId, storePhone, storeEmail, storeAddress, storeLogoUrl, storeManager_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (storeManagerName, storeManagerPssw, storeName, storeTaxId, storePhone, storeEmail, storeAddress, storeLogoUrl, storeManager_id))
            conn.commit()
            flash('Store Manager registration successful!', 'success')
        except psycopg2.IntegrityError:
            conn.rollback()
            flash('Store Manager registration failed. Please check your inputs.', 'danger')
        finally:
            cur.close()
            conn.close()

        return redirect(url_for('mainmenu.mainmenu'))

    return render_template('register_manager.html')