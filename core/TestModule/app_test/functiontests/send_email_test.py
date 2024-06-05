
# Import the necessary modules
import unittest

from core import send_simple_email
# Import the function to be tested
class TestSendEmail(unittest.TestCase):

    def test_send_email(self):
        print("Initing test send_email function")
        response_1 = send_simple_email('Unitary test', 'recipients@gmail.com', "This is a unitary test", False)
        self.assertEqual(response_1, True)
        print("Test send_email function completed")

unittest.main()
# What is the purpose of the test_send_email method?    
# The purpose of the test_send_email method is to test the send_email function to ensure that it correctly identifies the dominant emotion in the input text. The method uses assertions to compare the expected dominant emotion with the actual dominant emotion returned by the send_email function. This helps to verify the accuracy and functionality of the send_email function.

