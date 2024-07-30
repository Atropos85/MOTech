
from django.test import TestCase, Client
from ..models import APIKey, User


class APIKeyTest(TestCase):
    def setUp(self):
        # Crear un usuario de prueba
        self.user = User.objects.create(username='testuser')
        self.client = Client()
        # Generar una API Key para el usuario de prueba
        self.api_key = APIKey.objects.create(user=self.user)
    
    def test_valid_api_key(self):
        response = self.client.get(
            '/my-view/', 
            HTTP_X_API_KEY=self.api_key.key
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('Access granted', response.json()['message'])
    
    def test_invalid_api_key(self):
        response = self.client.get(
            'getcustomer/1/', 
            HTTP_X_API_KEY='invalidkey'
        )
        self.assertEqual(response.status_code, 403)
        self.assertIn('Invalid API Key', response.json()['error'])
    
    def test_missing_api_key(self):
        response = self.client.get('/my-view/')
        self.assertEqual(response.status_code, 403)
        self.assertIn('API Key required', response.json()['error'])
