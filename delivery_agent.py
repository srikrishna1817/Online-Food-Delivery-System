 
class DeliveryAgent:
    def __init__(self, agent_id, name):
        self.agent_id = agent_id
        self.name = name
        self.is_available = True

    def assign_delivery(self, order_id):
        if self.is_available:
            self.is_available = False
            return f"Order {order_id} assigned to {self.name}"
        return "Agent not available"

    def complete_delivery(self):
        self.is_available = True
        return "Delivery completed"