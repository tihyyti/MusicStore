from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_bcrypt import Bcrypt
import psycopg2
from datetime import datetime
from __init__ import db, logger

managerregist_bp = Blueprint('register_manager', __name__)
bcrypt = Bcrypt()

@managerregist_bp.route('/register_manager', methods=['GET', 'POST'])
def register_manager():
    if request.method == 'POST':
        storeManagerName = request.form['storeManagerName']
        storeManagerPassw = request.form['storeManagerPassw']
        storeName = request.form['storeName']
        storeTaxId = request.form['storeTaxId']
        storePhone = request.form['storePhone']
        storeEmail = request.form['storeEmail']
        storeAddress = request.form['storeAddress']
        storeLogoUrl = request.form.get('storeLogoUrl')
        storeManager_id = request.form["managers_customer_id"]

        # Hash the password
        storeManagerPsw = bcrypt.generate_password_hash(storeManagerPassw).decode("utf-8")

        last_login = datetime.now()
        conn = None
        cur = None

        try:
            conn = db.engine.raw_connection()
            cur = conn.cursor()
            logger.debug('db connected')

            cur.execute(
                """
                INSERT INTO mstore_v1.Store (storemanagername, storename, storetaxid,
                storephone, storeemail, storeaddress, storelogourl, storemanager_id,
                last_login, storemanagerpassw) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (
                    storeManagerName,
                    storeName,
                    storeTaxId,
                    storePhone,
                    storeEmail,
                    storeAddress,
                    storeLogoUrl,
                    storeManager_id,
                    last_login,
                    storeManagerPsw,
                ),
            )
            conn.commit()
            logger.debug("db committed successfully")
            flash('Store Manager registration successful!', 'success')

        except psycopg2.IntegrityError as e:
            if conn:
                conn.rollback()
            logger.error(f"IntegrityError: {e}")
            flash('Store Manager registration failed. Please check your inputs.', 'danger')
            return redirect(url_for('register_manager.register_manager'))

        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Error: {e}")
            flash('An error occurred. Please try again.', 'danger')
            return redirect(url_for('mainmenu.mainmenu'))

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
            return redirect(url_for('mainmenu.mainmenu'))

    return render_template('register_manager.html')
