class Wallet(object):
    def __init__(self, init_amt=0):
        self.balance = init_amt

    def withdraw(self, amt):
        if amt > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amt

    def deposit(self, amt):
        self.balance += amt
