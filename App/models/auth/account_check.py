from App.database.database_classes import Account

def check_account(username):
    account = Account.query.filter_by(username=username).first()
    if not account:
        return False
    return account