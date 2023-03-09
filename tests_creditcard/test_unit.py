from datetime import datetime
from django.test import TestCase

from creditcard_api.api import CreditcardViewSet

class AnimalTestCase(TestCase):
    def setUp(self):
        self.creditcardviewset = CreditcardViewSet()

    def test_get_brand(self):
        brand = self.creditcardviewset.get_brand('4593840058437546')

        self.assertEqual(brand, 'visa')
    
    def test_check_if_date_is_valid(self):
        response = self.creditcardviewset.check_if_date_is_valid('04/2023')

        self.assertEqual(response, None) 
    
    def test_check_if_date_is_invalid(self):
        response = self.creditcardviewset.check_if_date_is_valid('99992023')

        self.assertEqual(type(response), str)
    
    def test_check_if_date_is_not_lower_than_today(self):
        response = self.creditcardviewset.check_if_date_is_valid('10/2023')

        self.assertEqual(response, None)
    
    def test_check_if_date_is_lower_than_today(self):
        response = self.creditcardviewset.check_if_date_is_valid('02/2023')

        self.assertEqual(type(response), str)
    
    def test_normalize_date(self):
        my_date = datetime(2023, 3, 9)
        new_date = self.creditcardviewset.normalize_date(my_date)

        self.assertEqual(new_date.day, 1)
    
    def test_transform_date_field(self):
        date_text = '03/2023'
        new_date = self.creditcardviewset.transform_date_field(date_text)

        self.assertEqual(new_date, '2023-03-31')
    
    def test_encrypt_decrypt(self):
        card_number = '4593840058437548'
        encrypted_number = self.creditcardviewset.encrypt_number(card_number)
        decrypted_number = self.creditcardviewset.decrypt_number(encrypted_number)

        self.assertEqual(decrypted_number, card_number)


    
