from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from datetime import date
from django.utils import timezone
from rest_framework.reverse import reverse_lazy
from transliterate import translit

MINIMUM_SALARY = 24000.0


class Restaurant(models.Model):
    name = models.CharField(verbose_name="Название филиала", max_length=50, blank=False, null=False)
    address = models.TextField(verbose_name="Адрес ресторана", blank=False, null=False)
    phone = models.CharField(verbose_name="Номер телефона филиала", max_length=20, blank=False, null=False)
    email = models.EmailField(verbose_name="Почта филиала", max_length=50, unique=True)
    manager = models.ForeignKey('Employee', verbose_name="Менеджер филиала", on_delete=models.SET_NULL,
                                related_name='managed_restaurants', null=True, blank=True)
    slug = models.SlugField(default='', null=False, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(self.name, 'ru', reversed=True))
        super(Restaurant, self).save(*args, **kwargs)

    class Meta:
        indexes = [models.Index(fields=['name'])]
        verbose_name = "Ресторан"
        verbose_name_plural = "Рестораны"


class Table(models.Model):
    FREE = "FREE"
    OCCUPIED = "OCCUPIED"
    RESERVED = "RESERVED"
    STATUS_CHOICES = [(FREE, "Свободен"), (OCCUPIED, "Занят"), (RESERVED, "Зарезервирован")]
    restaurant = models.ForeignKey(Restaurant, verbose_name="Ресторан", on_delete=models.CASCADE, related_name='tables',
                                   null=False, blank=False)
    table_number = models.IntegerField(verbose_name="Номер стола", blank=False, null=False,
                                       validators=[MinValueValidator(1)])
    capacity = models.IntegerField(verbose_name="Вместимость стола", blank=False, null=False,
                                   validators=[MinValueValidator(1)])
    status = models.CharField(verbose_name="Статус", blank=False, null=False, choices=STATUS_CHOICES, max_length=10,
                              default=FREE)
    slug = models.SlugField(default='', null=False, unique=True)

    def __str__(self):
        return f"Стол {self.table_number} в {self.restaurant.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(f"{self.restaurant.name}-{self.table_number}", 'ru', reversed=True))
        super(Table, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('restaurant', 'table_number')
        indexes = [models.Index(fields=['restaurant', 'table_number'])]
        verbose_name = "Стол"
        verbose_name_plural = "Столы"


class Warehouse(models.Model):
    name = models.CharField(verbose_name="Название склада", max_length=50, blank=False, null=False)
    address = models.TextField(verbose_name="Адрес склада", blank=False, null=False)
    manager = models.ForeignKey('Employee', verbose_name="Менеджер склада", on_delete=models.SET_NULL,
                                related_name='managed_warehouses', null=True, blank=True)
    slug = models.SlugField(default='', null=False, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(self.name, 'ru', reversed=True))
        super(Warehouse, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"


class Employee(models.Model):
    first_name = models.CharField(verbose_name="Имя сотрудника", max_length=50, blank=False, null=False, db_index=True)
    last_name = models.CharField(verbose_name="Фамилия сотрудника", max_length=50, blank=False, null=False,
                                 db_index=True)
    role = models.CharField(verbose_name="Должность", max_length=50, blank=False, null=False)
    restaurant = models.ForeignKey(Restaurant, verbose_name="Ресторан", on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='employees')
    warehouse = models.ForeignKey(Warehouse, verbose_name="Склад", on_delete=models.CASCADE, null=True, blank=True,
                                  related_name='employees')
    hire_date = models.DateField(verbose_name="Дата трудоустройства", blank=False, null=False, default=date.today)
    salary = models.DecimalField(verbose_name="Зарплата", max_digits=10, decimal_places=2, blank=False, null=False,
                                 validators=[MinValueValidator(MINIMUM_SALARY)])
    slug = models.SlugField(default='', null=False, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        if self.restaurant:
            self.slug = slugify(
                translit(f"{self.first_name}-{self.last_name}-{self.restaurant.name}", 'ru', reversed=True))
        elif self.warehouse:
            self.slug = slugify(
                translit(f"{self.first_name}-{self.last_name}-{self.warehouse.name}", 'ru', reversed=True))
        else:
            self.slug = slugify(translit(f"{self.first_name}-{self.last_name}", 'ru', reversed=True))
        super(Employee, self).save(*args, **kwargs)

    def clean(self):
        if self.restaurant and self.warehouse:
            raise ValidationError("Сотрудник не может быть привязан одновременно к ресторану и складу.")

    def get_absolute_url(self):
        return reverse_lazy('detail_employee', args=(self.slug,))

    class Meta:
        indexes = [models.Index(fields=['first_name', 'last_name'])]
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        constraints = [
            models.CheckConstraint(check=models.Q(restaurant__isnull=True) | models.Q(warehouse__isnull=True),
                                   name='employee_single_assignment')]


class Supplier(models.Model):
    name = models.CharField(verbose_name="Имя поставщика", max_length=100, blank=False, null=False, unique=True,
                            db_index=True)
    contact_person = models.CharField(verbose_name="Представитель поставщика", max_length=100, blank=False, null=False)
    phone = models.CharField(verbose_name="Номер телефона поставщика", max_length=20, blank=False, null=False)
    email = models.EmailField(verbose_name="Почта поставщика", max_length=50, unique=True)
    address = models.TextField(verbose_name="Адрес поставщика", blank=False, null=False)
    slug = models.SlugField(default='', null=False, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(self.name, 'ru', reversed=True))
        super(Supplier, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"


class Product(models.Model):
    UNIT_KG = 'KG'
    UNIT_L = 'L'
    UNIT_PCS = 'PCS'
    UNIT_CHOICES = [(UNIT_KG, 'Килограммы'), (UNIT_L, 'Литры'), (UNIT_PCS, 'Штуки')]
    name = models.CharField(verbose_name="Название продукта", max_length=100, blank=False, null=False, unique=True,
                            db_index=True)
    unit = models.CharField(verbose_name="Единица измерения", max_length=20, blank=False, null=False,
                            choices=UNIT_CHOICES)
    supplier = models.ForeignKey(Supplier, verbose_name="Поставщик", on_delete=models.SET_NULL, null=True, blank=False,
                                 related_name='products')
    slug = models.SlugField(default='', null=False, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(self.name, 'ru', reversed=True))
        super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class Inventory(models.Model):
    warehouse = models.ForeignKey(Warehouse, verbose_name="Склад", on_delete=models.CASCADE, related_name='inventory',
                                  null=False, blank=False)
    product = models.ForeignKey(Product, verbose_name="Продукт", on_delete=models.CASCADE, related_name='inventory',
                                null=False, blank=False)
    quantity = models.DecimalField(verbose_name="Количество", max_digits=10, decimal_places=2, blank=False, null=False,
                                   validators=[MinValueValidator(0)])
    last_updated = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)
    slug = models.SlugField(default='', null=False, unique=True)

    def __str__(self):
        return f"{self.product.name} на {self.warehouse.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(f"{self.product.name}-{self.warehouse.name}", 'ru', reversed=True))
        super(Inventory, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('warehouse', 'product')
        indexes = [models.Index(fields=['warehouse', 'product'])]
        verbose_name = "Инвентарь"
        verbose_name_plural = "Инвентарь"


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, verbose_name="Ресторан", on_delete=models.CASCADE, related_name="menus",
                                   null=False, blank=False)
    name = models.CharField(verbose_name="Название меню", max_length=100, blank=False, null=False)
    description = models.TextField(verbose_name="Описание меню", blank=True, null=True)
    start_date = models.DateField(verbose_name="Дата ввода меню", blank=False, null=False, default=date.today)
    end_date = models.DateField(verbose_name="Дата отказа от меню", blank=True, null=True)
    slug = models.SlugField(default='', null=False, unique=True)

    def __str__(self):
        return f"{self.name} ({self.restaurant.name})"

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(f"{self.name}-{self.restaurant.name}", 'ru', reversed=True))
        super(Menu, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('restaurant', 'name')
        indexes = [models.Index(fields=['restaurant', 'name'])]
        verbose_name = "Меню"
        verbose_name_plural = "Меню"


class Dish(models.Model):
    name = models.CharField(verbose_name="Название блюда", max_length=100, blank=False, null=False, db_index=True)
    description = models.TextField(verbose_name="Описание блюда", blank=True, null=True)
    category = models.CharField(verbose_name="Категория", max_length=50, blank=True, null=True)
    base_price = models.DecimalField(verbose_name="Базовая цена", max_digits=10, decimal_places=2, blank=False,
                                     null=False, validators=[MinValueValidator(0)])
    slug = models.SlugField(default='', null=False, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(self.name, 'ru', reversed=True))
        super(Dish, self).save(*args, **kwargs)

    class Meta:
        indexes = [models.Index(fields=['name'])]
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"


class MenuDetail(models.Model):
    menu = models.ForeignKey(Menu, verbose_name="Меню", on_delete=models.CASCADE, related_name='details', null=False,
                             blank=False)
    dish = models.ForeignKey(Dish, verbose_name="Блюдо", on_delete=models.CASCADE, related_name='menu_details',
                             null=False, blank=False)
    price = models.DecimalField(verbose_name="Цена в меню", max_digits=10, decimal_places=2, blank=False, null=False,
                                validators=[MinValueValidator(0)])
    is_available = models.BooleanField(verbose_name="Доступно", default=True)

    class Meta:
        unique_together = ('menu', 'dish')
        indexes = [models.Index(fields=['menu', 'dish'])]
        verbose_name = "Деталь меню"
        verbose_name_plural = "Детали меню"


class Modifier(models.Model):
    name = models.CharField(verbose_name="Название модификатора", max_length=100, blank=False, null=False)
    price_change = models.DecimalField(verbose_name="Изменение цены", max_digits=10, decimal_places=2, default=0.0,
                                       validators=[MinValueValidator(0)])
    dish = models.ForeignKey(Dish, verbose_name="Блюдо", on_delete=models.CASCADE, related_name='modifiers', null=True,
                             blank=True)
    slug = models.SlugField(default='', null=False, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(translit(f"{self.name}-{self.dish.name if self.dish else 'generic'}", 'ru', reversed=True))
        super(Modifier, self).save(*args, **kwargs)

    class Meta:
        indexes = [models.Index(fields=['dish'])]
        verbose_name = "Модификатор"
        verbose_name_plural = "Модификаторы"


class Customer(models.Model):
    first_name = models.CharField(verbose_name="Имя клиента", max_length=50, blank=True, null=True)
    last_name = models.CharField(verbose_name="Фамилия клиента", max_length=50, blank=True, null=True)
    email = models.EmailField(verbose_name="Почта клиента", max_length=50, unique=True, blank=True, null=True)
    phone = models.CharField(verbose_name="Номер телефона клиента", max_length=20, blank=True, null=True)
    address = models.TextField(verbose_name="Адрес клиента", blank=True, null=True)
    slug = models.SlugField(default='', null=False, unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else (self.email
            or "Безымянный клиент")

    def save(self, *args, **kwargs):
        base = f"{self.first_name}-{self.last_name}" if self.first_name and self.last_name else (self.email
            or f"customer-{self.id or 'new'}")
        self.slug = slugify(translit(base, 'ru', reversed=True))
        super(Customer, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Reservation(models.Model):
    CONFIRMED = 'CONFIRMED'
    CANCELLED = 'CANCELLED'
    COMPLETED = 'COMPLETED'
    STATUS_CHOICES = [(CONFIRMED, 'Подтверждено'), (CANCELLED, 'Отменено'), (COMPLETED, 'Завершено')]
    table = models.ForeignKey(Table, verbose_name="Стол", on_delete=models.CASCADE, related_name='reservations',
                              null=False, blank=False)
    customer = models.ForeignKey(Customer, verbose_name="Клиент", on_delete=models.SET_NULL,
                                 related_name='reservations', null=True, blank=True)
    reservation_date = models.DateField(verbose_name="Дата бронирования", blank=False, null=False)
    time = models.TimeField(verbose_name="Время бронирования", blank=False, null=False)
    number_of_guests = models.IntegerField(verbose_name="Количество гостей", blank=False, null=False,
                                           validators=[MinValueValidator(1)])
    status = models.CharField(verbose_name="Статус", max_length=20, choices=STATUS_CHOICES, default=CONFIRMED)
    slug = models.SlugField(default='', null=False, unique=True)

    def __str__(self):
        return f"Бронирование на {self.reservation_date} {self.time} для {self.table}"

    def save(self, *args, **kwargs):
        self.slug = slugify(
            translit(f"{self.table.restaurant.name}-{self.table.table_number}-{self.reservation_date}", 'ru',
                     reversed=True))
        super(Reservation, self).save(*args, **kwargs)

    class Meta:
        indexes = [models.Index(fields=['table', 'reservation_date'])]
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"


class Order(models.Model):
    PENDING = 'PENDING'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'
    STATUS_CHOICES = [(PENDING, 'В обработке'), (COMPLETED, 'Завершён'), (CANCELLED, 'Отменён')]
    restaurant = models.ForeignKey(Restaurant, verbose_name="Ресторан", on_delete=models.CASCADE, related_name='orders',
                                   null=False, blank=False)
    customer = models.ForeignKey(Customer, verbose_name="Клиент", on_delete=models.SET_NULL, related_name='orders',
                                 null=True, blank=True)
    order_date = models.DateTimeField(verbose_name="Время заказа", blank=False, null=False, default=timezone.now)
    total_amount = models.DecimalField(verbose_name="Общая сумма", max_digits=10, decimal_places=2, blank=False,
                                       null=False, validators=[MinValueValidator(0)])
    status = models.CharField(verbose_name="Статус", max_length=20, choices=STATUS_CHOICES, default=PENDING)
    slug = models.SlugField(default='', null=False, unique=True)

    def __str__(self):
        return f"Заказ #{self.id} от {self.order_date.strftime('%Y-%m-%d %H:%M')}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                translit(f"payment-{self.restaurant.name}-{self.order_date.strftime('%Y%m%d%H%M%S')}", 'ru',
                         reversed=True))
        super(Order, self).save(*args, **kwargs)

    class Meta:
        indexes = [models.Index(fields=['restaurant', 'order_date'])]
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, verbose_name="Заказ", on_delete=models.CASCADE, related_name='details', null=False,
                              blank=False)
    dish = models.ForeignKey(Dish, verbose_name="Блюдо", on_delete=models.CASCADE, related_name='order_details',
                             null=False, blank=False)
    quantity = models.IntegerField(verbose_name="Количество", blank=False, null=False,
                                   validators=[MinValueValidator(1)])
    price = models.DecimalField(verbose_name="Цена", max_digits=10, decimal_places=2, blank=False, null=False,
                                validators=[MinValueValidator(0)])
    modifiers = models.JSONField(verbose_name="Модификаторы", null=True, blank=True)

    class Meta:
        indexes = [models.Index(fields=['order', 'dish'])]
        verbose_name = "Деталь заказа"
        verbose_name_plural = "Детали заказа"


class Payment(models.Model):
    CASH = 'CASH'
    CARD = 'CARD'
    ONLINE = 'ONLINE'
    PAYMENT_METHODS = [(CASH, 'Наличные'), (CARD, 'Карта'), (ONLINE, 'Онлайн')]
    order = models.ForeignKey(Order, verbose_name="Заказ", on_delete=models.CASCADE, related_name='payments',
                              null=False, blank=False)
    amount = models.DecimalField(verbose_name="Сумма", max_digits=10, decimal_places=2, blank=False, null=False,
                                 validators=[MinValueValidator(0)])
    payment_method = models.CharField(verbose_name="Способ оплаты", max_length=20, choices=PAYMENT_METHODS, blank=False,
                                      null=False)
    transaction_id = models.CharField(verbose_name="ID транзакции", max_length=100, blank=True, null=True)
    payment_time = models.DateTimeField(verbose_name="Время оплаты", blank=False, null=False, default=timezone.now)
    slug = models.SlugField(default='', null=False, unique=True)

    def __str__(self):
        return f"Платёж #{self.id} для заказа #{self.order.id}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                translit(f"payment-{self.order.restaurant.name}-{self.payment_time.strftime('%Y%m%d%H%M%S')}", 'ru',
                         reversed=True))
        super(Payment, self).save(*args, **kwargs)

    class Meta:
        indexes = [models.Index(fields=['order'])]
        verbose_name = "Платёж"
        verbose_name_plural = "Платежи"
