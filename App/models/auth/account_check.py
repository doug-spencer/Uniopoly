from App.models.classes.main import Account

def check_account(username):
    account = Account.query.filter_by(username=username).first()
    if not account:
        return False
    return account