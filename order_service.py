 
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
    

    def cancel_order(self, order_id):
        for order in self.orders:
            if order["order_id"] == order_id:
                order["status"] = "Cancelled"
                return f"Order {order_id} cancelled successfully"
        return "Order not found"

    def update_order_status(self, order_id, new_status):
        valid_statuses = ["Placed", "Preparing", "Out for Delivery", "Delivered"]
        if new_status not in valid_statuses:
            return "Invalid status"
        for order in self.orders:
            if order["order_id"] == order_id:
                order["status"] = new_status
                return f"Order {order_id} updated to {new_status}"
        return "Order not found"

    def apply_discount(self, order_id, discount_percentage):
        """Apply a percentage discount to an order.
        
        Args:
            order_id: The ID of the order to apply discount to
            discount_percentage: The discount percentage (0-100)
        
        Returns:
            Updated order with discount applied, or error message
        """
        if discount_percentage < 0 or discount_percentage > 100:
            return "Invalid discount percentage. Must be between 0 and 100"
        
        for order in self.orders:
            if order["order_id"] == order_id:
                # Calculate total amount from items (assuming items have 'price' field)
                total = sum(item.get("price", 0) for item in order["items"])
                discount_amount = total * (discount_percentage / 100)
                final_price = total - discount_amount
                
                order["original_total"] = total
                order["discount_percentage"] = discount_percentage
                order["discount_amount"] = discount_amount
                order["final_price"] = final_price
                return order
        
        return "Order not found"