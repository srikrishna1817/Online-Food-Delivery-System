import unittest
from payment import PaymentService


class TestPaymentService(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.payment_service = PaymentService()

    def test_process_payment_success(self):
        """Test processing a payment successfully."""
        result = self.payment_service.process_payment(1, 100.00, "Credit Card")
        
        self.assertEqual(result["order_id"], 1)
        self.assertEqual(result["amount"], 100.00)
        self.assertEqual(result["method"], "Credit Card")
        self.assertEqual(result["status"], "Success")

    def test_process_payment_adds_transaction(self):
        """Test that processing a payment adds a transaction to the list."""
        self.payment_service.process_payment(1, 50.00, "Cash")
        self.payment_service.process_payment(2, 75.00, "Debit Card")
        
        self.assertEqual(len(self.payment_service.transactions), 2)

    def test_get_transaction_existing(self):
        """Test retrieving an existing transaction."""
        self.payment_service.process_payment(1, 100.00, "Credit Card")
        result = self.payment_service.get_transaction(1)
        
        self.assertIsNotNone(result)
        self.assertEqual(result["order_id"], 1)
        self.assertEqual(result["amount"], 100.00)

    def test_get_transaction_nonexistent(self):
        """Test retrieving a non-existent transaction."""
        result = self.payment_service.get_transaction(999)
        
        self.assertIsNone(result)

    def test_refund_payment_success(self):
        """Test refunding an existing payment."""
        self.payment_service.process_payment(1, 100.00, "Credit Card")
        result = self.payment_service.refund_payment(1)
        
        self.assertEqual(result, "Order 1 refunded successfully")
        
        # Verify the transaction status is updated
        transaction = self.payment_service.get_transaction(1)
        self.assertEqual(transaction["status"], "Refunded")

    def test_refund_payment_nonexistent(self):
        """Test refunding a non-existent payment."""
        result = self.payment_service.refund_payment(999)
        
        self.assertEqual(result, "Transaction not found")

    def test_get_payment_summary_no_transactions(self):
        """Test payment summary with no transactions."""
        result = self.payment_service.get_payment_summary()
        
        self.assertEqual(result, "Total transactions: 0, Total amount: 0")

    def test_get_payment_summary_with_transactions(self):
        """Test payment summary with multiple transactions."""
        self.payment_service.process_payment(1, 100.00, "Credit Card")
        self.payment_service.process_payment(2, 50.00, "Cash")
        self.payment_service.process_payment(3, 75.00, "Debit Card")
        
        result = self.payment_service.get_payment_summary()
        
        self.assertEqual(result, "Total transactions: 3, Total amount: 225.0")

    def test_process_payment_with_various_methods(self):
        """Test processing payments with different payment methods."""
        methods = ["Credit Card", "Debit Card", "Cash", "PayPal", "Crypto"]
        
        for i, method in enumerate(methods, 1):
            result = self.payment_service.process_payment(i, 100.00, method)
            self.assertEqual(result["method"], method)

    def test_refund_already_refunded(self):
        """Test refunding an already refunded payment."""
        self.payment_service.process_payment(1, 100.00, "Credit Card")
        self.payment_service.refund_payment(1)
        self.payment_service.refund_payment(1)
        
        transaction = self.payment_service.get_transaction(1)
        self.assertEqual(transaction["status"], "Refunded")


if __name__ == "__main__":
    unittest.main()