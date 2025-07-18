from rest_framework import serializers
from .models import (
    Restaurant, Table, Warehouse, Employee, Supplier, Product, Inventory,
    Menu, Dish, MenuDetail, Modifier, Customer, Reservation, Order, OrderDetail, Payment
)
from rest_framework.serializers import (
    ModelSerializer, CharField, SlugRelatedField, PrimaryKeyRelatedField,
    DecimalField, IntegerField, DateField, TimeField, DateTimeField, JSONField, BooleanField
)
from django.core.exceptions import ValidationError


class RestaurantSerializer(ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'phone', 'email', 'manager', 'slug']


class TableSerializer(ModelSerializer):
    restaurant = SlugRelatedField(slug_field='slug', queryset=Restaurant.objects.all())

    class Meta:
        model = Table
        fields = ['id', 'restaurant', 'table_number', 'capacity', 'status', 'slug']


class WarehouseSerializer(ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id', 'name', 'address', 'manager', 'slug']


class EmployeeSerializer(ModelSerializer):
    restaurant = SlugRelatedField(slug_field='slug', queryset=Restaurant.objects.all(), required=False, allow_null=True)
    warehouse = SlugRelatedField(slug_field='slug', queryset=Warehouse.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'role', 'restaurant', 'warehouse', 'hire_date', 'salary', 'slug']

    def validate(self, data):
        if data.get('restaurant') and data.get('warehouse'):
            raise ValidationError("Сотрудник не может быть привязан одновременно к ресторану и складу.")
        return data


class SupplierSerializer(ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'contact_person', 'phone', 'email', 'address', 'slug']


class ProductSerializer(ModelSerializer):
    supplier = SlugRelatedField(slug_field='slug', queryset=Supplier.objects.all(), allow_null=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'unit', 'supplier', 'slug']


class InventorySerializer(ModelSerializer):
    warehouse = SlugRelatedField(slug_field='slug', queryset=Warehouse.objects.all())
    product = SlugRelatedField(slug_field='slug', queryset=Product.objects.all())

    class Meta:
        model = Inventory
        fields = ['id', 'warehouse', 'product', 'quantity', 'last_updated', 'slug']


class MenuSerializer(ModelSerializer):
    restaurant = SlugRelatedField(slug_field='slug', queryset=Restaurant.objects.all())

    class Meta:
        model = Menu
        fields = ['id', 'restaurant', 'name', 'description', 'start_date', 'end_date', 'slug']


class DishSerializer(ModelSerializer):
    class Meta:
        model = Dish
        fields = ['id', 'name', 'description', 'category', 'base_price', 'slug']


class MenuDetailSerializer(ModelSerializer):
    menu = SlugRelatedField(slug_field='slug', queryset=Menu.objects.all())
    dish = SlugRelatedField(slug_field='slug', queryset=Dish.objects.all())

    class Meta:
        model = MenuDetail
        fields = ['id', 'menu', 'dish', 'price', 'is_available']


class ModifierSerializer(ModelSerializer):
    dish = SlugRelatedField(slug_field='slug', queryset=Dish.objects.all(), allow_null=True)

    class Meta:
        model = Modifier
        fields = ['id', 'name', 'price_change', 'dish', 'slug']


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name', 'email', 'phone', 'address', 'slug']


class ReservationSerializer(ModelSerializer):
    table = SlugRelatedField(slug_field='slug', queryset=Table.objects.all())
    customer = SlugRelatedField(slug_field='slug', queryset=Customer.objects.all(), allow_null=True)

    class Meta:
        model = Reservation
        fields = ['id', 'table', 'customer', 'reservation_date', 'time', 'number_of_guests', 'status', 'slug']

    def validate(self, data):
        table = data.get('table')
        reservation_date = data.get('reservation_date')
        time = data.get('time')
        if table and reservation_date and time:
            conflicting_reservations = Reservation.objects.filter(
                table=table,
                reservation_date=reservation_date,
                time=time,
                status=Reservation.CONFIRMED
            ).exclude(pk=self.instance.pk if self.instance else None)
            if conflicting_reservations.exists():
                raise ValidationError("Стол уже забронирован на это время.")
        return data


class OrderDetailSerializer(ModelSerializer):
    dish = SlugRelatedField(slug_field='slug', queryset=Dish.objects.all())

    class Meta:
        model = OrderDetail
        fields = ['id', 'order', 'dish', 'quantity', 'price', 'modifiers']


class OrderSerializer(ModelSerializer):
    restaurant = SlugRelatedField(slug_field='slug', queryset=Restaurant.objects.all())
    customer = SlugRelatedField(slug_field='slug', queryset=Customer.objects.all(), allow_null=True)
    details = OrderDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'restaurant', 'customer', 'order_date', 'total_amount', 'status', 'slug', 'details']


class PaymentSerializer(ModelSerializer):
    order = SlugRelatedField(slug_field='slug', queryset=Order.objects.all())

    class Meta:
        model = Payment
        fields = ['id', 'order', 'amount', 'payment_method', 'transaction_id', 'payment_time', 'slug']


"""
class EmployeeSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    role = serializers.CharField()
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all(),required=False)
    warehouse = serializers.PrimaryKeyRelatedField(queryset=Warehouse.objects.all(),required=False)
    hire_date = serializers.DateField(required=False)
    salary = serializers.FloatField()
    slug = serializers.SlugField(required=False)

    def create(self, validated_data):
        return Employee.objects.create(**validated_data)

    def update(self, instance: Employee, validated_data: dict):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.role = validated_data.get('role', instance.role)
        instance.restaurant = validated_data.get('restaurant', instance.restaurant)
        instance.warehouse = validated_data.get('warehouse', instance.warehouse)
        instance.hire_date = validated_data.get('hire_date', instance.hire_date)
        instance.salary = validated_data.get('salary', instance.salary)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.save()
        return instance

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
        extra_kwargs = {
            'restaurant': {'required': False},
            'warehouse': {'required': False},
            'hire_date': {'required': False},
            'slug': {'required': False},
        }"""
