# flake8: noqa
class TransactionsModel:
    def __init__(self, date, event, investment, quantity, price, amount):
        self.date = date
        self.event = event
        self.investment = investment
        self.quantity = quantity
        self.price = price
        self.amount = amount
