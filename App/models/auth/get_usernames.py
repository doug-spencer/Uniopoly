from App.database.database_classes import Account

def get_account_usernames():
    accounts = Account.query.all()
    account_usernames = []
    for i in accounts:
        account_usernames.append(i.username)
    print(account_usernames)
    return account_usernames