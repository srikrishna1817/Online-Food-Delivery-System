 
class PaymentService:
    def __init__(self):
        self.transactions = []

    def process_payment(self, order_id, amount, method):
        transaction = {
            "order_id": order_id,
            "amount": amount,
            "method": method,
            "status": "Success"
        }
        self.transactions.append(transaction)
        return transaction

    def get_transaction(self, order_id):
        for t in self.transactions:
            if t["order_id"] == order_id:
                return t
        return None