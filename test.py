
class DataBaseTester:

    @staticmethod
    def create_accounts(times: int, account_model, db, namebase='user'):
        for i in range(times):
            account = account_model(name = f"{namebase}{i}", password = f"{namebase}{i}")
            db.session.add(account)
        db.session.commit()

