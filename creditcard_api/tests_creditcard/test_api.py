import copy
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase

class ProductTests(APITestCase):
    def setUp(self):
        self.api_url = '/api/creditcards/'
        self.super_user = self.create_superuser()
        self.client.force_authenticate(user=self.super_user)
        self.default_creditcard = {
            "exp_date": "04/2023",
            "holder": "Teste",
            "number": "4593840058437546",
            "cvv": "123"
        }

    def create_superuser(self):
        return User.objects.create_superuser(username='daniel', password='123', email='')

    def test_create_creditcard(self):
        response = self.create_creditcard()
        desired_response = {
            "success": True,
            "message": "Creditcard created successfully!"
        }
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), desired_response)
    
    def test_list_creditcard(self):
        self.create_creditcard()

        response = self.client.get(self.api_url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_get_single_creditcard(self):
        self.create_creditcard()

        response = self.client.get(f'{self.api_url}1/', format='json')

        desired_response = {
            "exp_date": "2023-04-30",
            "holder": "Teste",
            "number": "4593840058437546",
            "cvv": 123,
            "brand": "visa",
            "id": 1
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), desired_response)
    
    def create_creditcard(self):
        data = copy.deepcopy(self.default_creditcard)
        
        response = self.client.post(self.api_url, data, format='json')
        return response