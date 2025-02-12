from werkzeug.security import check_password_hash
from models import Account

def verify_account(verifiable_acc, password):
    print(verifiable_acc.password)
    if check_password_hash(verifiable_acc.password, password) == True:
        print('verified')
        return True
    else:
        return False