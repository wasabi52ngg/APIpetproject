import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from first_app.models import Restaurant, Employee, Table, Reservation, Order, Customer
from datetime import date, time
from django.utils import timezone


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db):
    return User.objects.create_user(username='testuser', password='testpass')


@pytest.fixture
def create_authenticated_client(api_client, create_user):
    api_client.post('api/v1/auth/', {'username': 'testuser', 'password': 'testpass'})
    response = api_client.post('/auth/token/login/', {'username': 'testuser', 'password': 'testpass'})
    token = response.data['auth_token']
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    return api_client


@pytest.fixture
def create_restaurant(db):
    return Restaurant.objects.create(
        name="Test Restaurant",
        address="123 Test St",
        phone="1234567890",
        email="test@restaurant.com",
        slug="test-restaurant"
    )


@pytest.fixture
def create_employee(create_restaurant):
    return Employee.objects.create(
        first_name="John",
        last_name="Doe",
        role="Manager",
        restaurant=create_restaurant,
        salary=30000,
        slug="john-doe-test-restaurant"
    )


@pytest.fixture
def create_table(create_restaurant):
    return Table.objects.create(
        restaurant=create_restaurant,
        table_number="1",
        capacity=4,
        status=Table.FREE,
        slug="table-1-test-restaurant"
    )


@pytest.fixture
def create_customer(db):
    return Customer.objects.create(
        first_name="Jane",
        last_name="Smith",
        email="jane@example.com",
        phone="9876543210",
        slug="jane-smith"
    )


@pytest.fixture
def create_reservation(create_table, create_customer):
    return Reservation.objects.create(
        table=create_table,
        customer=create_customer,
        reservation_date=date(2025, 7, 18),
        time=time(18, 0),
        number_of_guests=4,
        status=Reservation.CONFIRMED,
        slug="reservation-2025-07-18"
    )


@pytest.fixture
def create_order(create_restaurant, create_customer):
    return Order.objects.create(
        restaurant=create_restaurant,
        customer=create_customer,
        order_date=timezone.now(),
        total_amount=100.00,
        status=Order.PENDING,
        slug="order-2025-07-18"
    )


@pytest.mark.django_db
def test_restaurant_list(api_client, create_restaurant):
    url = reverse('restaurant-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['name'] == "Test Restaurant"


@pytest.mark.django_db
def test_restaurant_create_authenticated(create_authenticated_client, create_user):
    url = reverse('restaurant-list')
    data = {
        "name": "New Restaurant",
        "address": "456 New St",
        "phone": "0987654321",
        "email": "new@restaurant.com",
        "slug": "new-restaurant"
    }
    response = create_authenticated_client.post(url, data, format='json')
    assert response.status_code == 201
    assert response.data['name'] == "New Restaurant"


@pytest.mark.django_db
def test_restaurant_create_unauthenticated(api_client):
    url = reverse('restaurant-list')
    data = {
        "name": "New Restaurant",
        "address": "456 New St",
        "phone": "0987654321",
        "email": "new@restaurant.com",
        "slug": "new-restaurant"
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == 401


@pytest.mark.django_db
def test_employee_salary_filter(create_authenticated_client, create_employee):
    url = reverse('employee-list') + '?salary__gt=25000'
    response = create_authenticated_client.get(url)
    assert response.status_code == 200
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['first_name'] == "John"


@pytest.mark.django_db
def test_employee_salary_filter_no_results(create_authenticated_client, create_employee):
    url = reverse('employee-list') + '?salary__gt=50000'
    response = create_authenticated_client.get(url)
    assert response.status_code == 200
    assert len(response.data['results']) == 0


@pytest.mark.django_db
def test_employee_search(create_authenticated_client, create_employee):
    url = reverse('employee-list') + '?search=John'
    response = create_authenticated_client.get(url)
    assert response.status_code == 200
    assert len(response.data['results']) == 1
    assert response.data['results'][0]['first_name'] == "John"


@pytest.mark.django_db
def test_employee_ordering(create_authenticated_client, create_employee):
    Employee.objects.create(
        first_name="Alice",
        last_name="Smith",
        role="Waiter",
        restaurant=create_employee.restaurant,
        salary=20000,
        slug="alice-smith-test-restaurant"
    )
    url = reverse('employee-list') + '?ordering=-salary'
    response = create_authenticated_client.get(url)
    assert response.status_code == 200
    assert response.data['results'][0]['first_name'] == "John"


@pytest.mark.django_db
def test_table_set_status(create_authenticated_client, create_table):
    url = reverse('table-set-status', kwargs={'pk': create_table.pk})
    data = {"status": Table.OCCUPIED}
    response = create_authenticated_client.post(url, data, format='json')
    assert response.status_code == 200
    assert response.data['status'] == Table.OCCUPIED
    create_table.refresh_from_db()
    assert create_table.status == Table.OCCUPIED


@pytest.mark.django_db
def test_table_set_status_unauthenticated(api_client, create_table):
    url = reverse('table-set-status', kwargs={'pk': create_table.pk})
    data = {"status": Table.OCCUPIED}
    response = api_client.post(url, data, format='json')
    assert response.status_code == 401


# @pytest.mark.django_db
# def test_reservation_cancel(create_authenticated_client, create_reservation, create_table):
#     url = reverse('reservation-cancel', kwargs={'pk': create_reservation.pk})
#     response = create_authenticated_client.post(url)
#     assert response.status_code == 200
#     assert response.data['status'] == Reservation.CANCELLED
#     create_reservation.refresh_from_db()
#     create_table.refresh_from_db()
#     assert create_reservation.status == Reservation.CANCELLED
#     assert create_table.status == Table.FREE
#
#
# @pytest.mark.django_db
# def test_reservation_cancel_invalid_status(create_authenticated_client, create_reservation):
#     create_reservation.status = Reservation.CANCELLED
#     create_reservation.save()
#     url = reverse('reservation-cancel', kwargs={'pk': create_reservation.pk})
#     response = create_authenticated_client.post(url)
#     assert response.status_code == 400
#     assert 'error' in response.data


@pytest.mark.django_db
def test_order_complete(create_authenticated_client, create_order):
    url = reverse('order-complete', kwargs={'pk': create_order.pk})
    response = create_authenticated_client.post(url)
    assert response.status_code == 200
    assert response.data['status'] == Order.COMPLETED
    create_order.refresh_from_db()
    assert create_order.status == Order.COMPLETED


@pytest.mark.django_db
def test_order_complete_invalid_status(create_authenticated_client, create_order):
    create_order.status = Order.COMPLETED
    create_order.save()
    url = reverse('order-complete', kwargs={'pk': create_order.pk})
    response = create_authenticated_client.post(url)
    assert response.status_code == 400
    assert 'error' in response.data


@pytest.mark.django_db
def test_token_login(api_client, create_user):
    response = api_client.post('/auth/token/login/', {'username': 'testuser', 'password': 'testpass'})
    assert response.status_code == 200
    assert 'auth_token' in response.data


@pytest.mark.django_db
def test_token_login_invalid_credentials(api_client):
    response = api_client.post('/auth/token/login/', {'username': 'wronguser', 'password': 'wrongpass'})
    assert response.status_code == 400
