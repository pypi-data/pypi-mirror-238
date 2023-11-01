import unittest

from rabbitmq_helpers import get_messages_from_queue, push_to_queue


class IntegrationTestRabbitMQHelpers(unittest.TestCase):
    """Test class to ensure pushing & reading from queue works as expected."""

    @classmethod
    def setUpClass(cls):
        """Setup once for all tests"""
        cls.queue_name = "updaters_integration_tests"

    def test_push_and_get_message(self):
        """Push a message and then get it from the queue"""

        # Given a message
        test_message = "Integration test message"

        # When pushing the message to the queue
        push_to_queue(self.queue_name, test_message)

        # Then it should be retrieved from the queue
        messages = get_messages_from_queue(self.queue_name, queue_batch_size=1)
        self.assertIn(test_message, messages)

    @classmethod
    def tearDownClass(cls):
        """Cleanup once after all tests"""
        # Optionally, you can clear the queue if required
        while get_messages_from_queue(cls.queue_name, queue_batch_size=1):
            pass

if __name__ == '__main__':
    unittest.main()
