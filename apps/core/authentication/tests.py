from django.test import TestCase
from django.urls import reverse

class AuthTestCase(TestCase):
    def test_login(self):
        response = self.client.post(reverse("login"), {
            "user-login": "testuser", 
            "password": "12345678"
        })
        self.assertEqual(response.status_code, 302)
        
    def test_protected_route(self):
        self.client.post(reverse("login"), {
            "user-login": "testuser", 
            "password": "12345678"
        })
        response = self.client.get(reverse("protected-route"))
        self.assertEqual(response.status_code, 302)




