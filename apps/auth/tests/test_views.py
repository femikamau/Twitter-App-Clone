from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

User = get_user_model()


class AuthViewsTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {
            "email": "testuser@email.com",
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser",
            "password1": "testpassword123",
            "password2": "testpassword123",
        }

        cls.login_data = {
            "username": "testuser",
            "password": "testpassword123",
        }

    def test_register(self):
        url = reverse("register")

        response = self.client.post(url, data=self.user_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_login(self):
        self.client.post(reverse("register"), data=self.user_data)

        url = reverse("login")

        # Assert that the wrong credentials won't work

        response = self.client.post(
            url, data={**self.login_data, "password": "wrongpassword"}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Assert that the correct credentials will work

        response = self.client.post(url, data=self.login_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("token" in response.data)
        self.assertTrue(Token.objects.filter(user__username="testuser").exists())

    def test_logout(self):
        self.client.post(reverse("register"), data=self.user_data)

        url = reverse("login")

        response = self.client.post(url, data=self.login_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("token" in response.data)
        self.assertTrue(Token.objects.filter(user__username="testuser").exists())

        url = reverse("logout")

        response = self.client.delete(
            url, HTTP_AUTHORIZATION=f"Token {response.data['token']}"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Token.objects.filter(user__username="testuser").exists())
