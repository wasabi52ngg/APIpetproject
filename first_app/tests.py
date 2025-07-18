from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import Employee, Restaurant
from rest_framework.test import APIClient
from django.urls import reverse


# Create your tests here.

class GetPagesTestCase(TestCase):
    def setUp(self):
        "Инициализация перед выполнением каждого теста"

    def test_case_1(self):
        pass

    def test_case_2(self):
        pass

    def test_create_employee(self):
        Employee.objects.create(
            first_name="John",
            last_name="Doe",
            role="Manager",
            restaurant=Restaurant.objects.create(
                name="Test Restaurant",
                address="123 Test St",
                phone="1234567890",
                email="test@restaurant.com",
                slug="test-restaurant"
            ),
            salary=30000,
            slug="john-doe-test-restaurant"
        )
        self.assertNotEqual(Employee.objects.all(), None)

    def test_access_to_employee(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        response = self.client.post('/auth/token/login/', data={'username': 'testuser', 'password': 'testpass'})
        token = response.data['auth_token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(self.client.get(reverse('employee-list')).status_code, 200)

    def tearDown(self):
        "Действия после выполнения каждого теста"
