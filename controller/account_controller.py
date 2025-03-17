from flask import render_template, request
from flask_login import current_user

from repository.account_repository import AccountAccess, Account

def profile_page(user_id):
    profile_owner = AccountAccess.get_record_by_id(Account, user_id)
    if request.method == 'POST' and current_user.is_authenticated:
        form_type = request.form['form_type']
        if form_type == 'follow':
            AccountAccess.follow_to_account(current_user, profile_owner)



    return render_template('profile_page.html', user=profile_owner)
