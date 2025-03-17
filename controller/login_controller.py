from flask import request, redirect, url_for, render_template
from repository import AccountAccess
from models import Account
from functions import get_name_and_password_from_form
from flask_login import login_user, logout_user

def sign_up_page():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        is_successfully_created = AccountAccess.create_account(name, password)
        if is_successfully_created:
            return redirect(url_for('sign_in'))
        elif not is_successfully_created:
            return redirect(url_for('sign_up'))
    return render_template('sign_up.html')

def sign_in_page():
    if request.method == 'POST':
        name, password = get_name_and_password_from_form(request.form)
        orig_account = AccountAccess.get_record_by(Account, name=name)
        if AccountAccess.verify_user_by_password(orig_account, password):
            login_user(orig_account)
            return redirect(url_for('home'))
        return 'не удалось войти'
    return render_template('sign_in.html')

def sign_out_page():
    logout_user()
    return redirect(url_for('home'))