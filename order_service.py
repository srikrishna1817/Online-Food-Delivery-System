 
class OrderService:
    def __init__(self):
        self.orders = []

    def place_order(self, customer_id, items):
        order = {
            "order_id": len(self.orders) + 1,
            "customer_id": customer_id,
            "items": items,
            "status": "Placed"
        }
        self.orders.append(order)
        return order

    def get_order_status(self, order_id):
        for order in self.orders:
            if order["order_id"] == order_id:
                return order["status"]
        return "Order not found"