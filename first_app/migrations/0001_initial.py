# Generated by Django 5.2 on 2025-07-07 05:14

import datetime
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Имя клиента')),
                ('last_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Фамилия клиента')),
                ('email', models.EmailField(blank=True, max_length=50, null=True, unique=True, verbose_name='Почта клиента')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Номер телефона клиента')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Адрес клиента')),
                ('slug', models.SlugField(default='', unique=True)),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(db_index=True, max_length=50, verbose_name='Имя сотрудника')),
                ('last_name', models.CharField(db_index=True, max_length=50, verbose_name='Фамилия сотрудника')),
                ('role', models.CharField(max_length=50, verbose_name='Должность')),
                ('hire_date', models.DateField(default=datetime.date.today, verbose_name='Дата трудоустройства')),
                ('salary', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(24000.0)], verbose_name='Зарплата')),
                ('slug', models.SlugField(default='', unique=True)),
            ],
            options={
                'verbose_name': 'Сотрудник',
                'verbose_name_plural': 'Сотрудники',
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, unique=True, verbose_name='Имя поставщика')),
                ('contact_person', models.CharField(max_length=100, verbose_name='Представитель поставщика')),
                ('phone', models.CharField(max_length=20, verbose_name='Номер телефона поставщика')),
                ('email', models.EmailField(max_length=50, unique=True, verbose_name='Почта поставщика')),
                ('address', models.TextField(verbose_name='Адрес поставщика')),
                ('slug', models.SlugField(default='', unique=True)),
            ],
            options={
                'verbose_name': 'Поставщик',
                'verbose_name_plural': 'Поставщики',
            },
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='Название блюда')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание блюда')),
                ('category', models.CharField(blank=True, max_length=50, null=True, verbose_name='Категория')),
                ('base_price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Базовая цена')),
                ('slug', models.SlugField(default='', unique=True)),
            ],
            options={
                'verbose_name': 'Блюдо',
                'verbose_name_plural': 'Блюда',
                'indexes': [models.Index(fields=['name'], name='first_app_d_name_2069e8_idx')],
            },
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название филиала')),
                ('address', models.TextField(verbose_name='Адрес ресторана')),
                ('phone', models.CharField(max_length=20, verbose_name='Номер телефона филиала')),
                ('email', models.EmailField(max_length=50, unique=True, verbose_name='Почта филиала')),
                ('slug', models.SlugField(default='', unique=True)),
                ('manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='managed_restaurants', to='first_app.employee', verbose_name='Менеджер филиала')),
            ],
            options={
                'verbose_name': 'Ресторан',
                'verbose_name_plural': 'Рестораны',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Время заказа')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Общая сумма')),
                ('status', models.CharField(choices=[('PENDING', 'В обработке'), ('COMPLETED', 'Завершён'), ('CANCELLED', 'Отменён')], default='PENDING', max_length=20, verbose_name='Статус')),
                ('slug', models.SlugField(default='', unique=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='first_app.customer', verbose_name='Клиент')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='first_app.restaurant', verbose_name='Ресторан')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название меню')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание меню')),
                ('start_date', models.DateField(default=datetime.date.today, verbose_name='Дата ввода меню')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='Дата отказа от меню')),
                ('slug', models.SlugField(default='', unique=True)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menus', to='first_app.restaurant', verbose_name='Ресторан')),
            ],
            options={
                'verbose_name': 'Меню',
                'verbose_name_plural': 'Меню',
            },
        ),
        migrations.AddField(
            model_name='employee',
            name='restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='first_app.restaurant', verbose_name='Ресторан'),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, unique=True, verbose_name='Название продукта')),
                ('unit', models.CharField(choices=[('KG', 'Килограммы'), ('L', 'Литры'), ('PCS', 'Штуки')], max_length=20, verbose_name='Единица измерения')),
                ('slug', models.SlugField(default='', unique=True)),
                ('supplier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='first_app.supplier', verbose_name='Поставщик')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
            },
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_number', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Номер стола')),
                ('capacity', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Вместимость стола')),
                ('status', models.CharField(choices=[('FREE', 'Свободен'), ('OCCUPIED', 'Занят'), ('RESERVED', 'Зарезервирован')], default='FREE', max_length=10, verbose_name='Статус')),
                ('slug', models.SlugField(default='', unique=True)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tables', to='first_app.restaurant', verbose_name='Ресторан')),
            ],
            options={
                'verbose_name': 'Стол',
                'verbose_name_plural': 'Столы',
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reservation_date', models.DateField(verbose_name='Дата бронирования')),
                ('time', models.TimeField(verbose_name='Время бронирования')),
                ('number_of_guests', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Количество гостей')),
                ('status', models.CharField(choices=[('CONFIRMED', 'Подтверждено'), ('CANCELLED', 'Отменено'), ('COMPLETED', 'Завершено')], default='CONFIRMED', max_length=20, verbose_name='Статус')),
                ('slug', models.SlugField(default='', unique=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reservations', to='first_app.customer', verbose_name='Клиент')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='first_app.table', verbose_name='Стол')),
            ],
            options={
                'verbose_name': 'Бронирование',
                'verbose_name_plural': 'Бронирования',
            },
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название склада')),
                ('address', models.TextField(verbose_name='Адрес склада')),
                ('slug', models.SlugField(default='', unique=True)),
                ('manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='managed_warehouses', to='first_app.employee', verbose_name='Менеджер склада')),
            ],
            options={
                'verbose_name': 'Склад',
                'verbose_name_plural': 'Склады',
            },
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Количество')),
                ('last_updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('slug', models.SlugField(default='', unique=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to='first_app.product', verbose_name='Продукт')),
                ('warehouse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to='first_app.warehouse', verbose_name='Склад')),
            ],
            options={
                'verbose_name': 'Инвентарь',
                'verbose_name_plural': 'Инвентарь',
            },
        ),
        migrations.AddField(
            model_name='employee',
            name='warehouse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='first_app.warehouse', verbose_name='Склад'),
        ),
        migrations.CreateModel(
            name='MenuDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена в меню')),
                ('is_available', models.BooleanField(default=True, verbose_name='Доступно')),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_details', to='first_app.dish', verbose_name='Блюдо')),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='first_app.menu', verbose_name='Меню')),
            ],
            options={
                'verbose_name': 'Деталь меню',
                'verbose_name_plural': 'Детали меню',
                'indexes': [models.Index(fields=['menu', 'dish'], name='first_app_m_menu_id_9b9bb1_idx')],
                'unique_together': {('menu', 'dish')},
            },
        ),
        migrations.CreateModel(
            name='Modifier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название модификатора')),
                ('price_change', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Изменение цены')),
                ('slug', models.SlugField(default='', unique=True)),
                ('dish', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modifiers', to='first_app.dish', verbose_name='Блюдо')),
            ],
            options={
                'verbose_name': 'Модификатор',
                'verbose_name_plural': 'Модификаторы',
                'indexes': [models.Index(fields=['dish'], name='first_app_m_dish_id_238cc8_idx')],
            },
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Количество')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена')),
                ('modifiers', models.JSONField(blank=True, null=True, verbose_name='Модификаторы')),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_details', to='first_app.dish', verbose_name='Блюдо')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='first_app.order', verbose_name='Заказ')),
            ],
            options={
                'verbose_name': 'Деталь заказа',
                'verbose_name_plural': 'Детали заказа',
                'indexes': [models.Index(fields=['order', 'dish'], name='first_app_o_order_i_ec85ec_idx')],
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Сумма')),
                ('payment_method', models.CharField(choices=[('CASH', 'Наличные'), ('CARD', 'Карта'), ('ONLINE', 'Онлайн')], max_length=20, verbose_name='Способ оплаты')),
                ('transaction_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='ID транзакции')),
                ('payment_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Время оплаты')),
                ('slug', models.SlugField(default='', unique=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='first_app.order', verbose_name='Заказ')),
            ],
            options={
                'verbose_name': 'Платёж',
                'verbose_name_plural': 'Платежи',
                'indexes': [models.Index(fields=['order'], name='first_app_p_order_i_bbd7fc_idx')],
            },
        ),
        migrations.AddIndex(
            model_name='restaurant',
            index=models.Index(fields=['name'], name='first_app_r_name_e5c552_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['restaurant', 'order_date'], name='first_app_o_restaur_df6798_idx'),
        ),
        migrations.AddIndex(
            model_name='menu',
            index=models.Index(fields=['restaurant', 'name'], name='first_app_m_restaur_b2fa2d_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='menu',
            unique_together={('restaurant', 'name')},
        ),
        migrations.AddIndex(
            model_name='table',
            index=models.Index(fields=['restaurant', 'table_number'], name='first_app_t_restaur_122ad9_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='table',
            unique_together={('restaurant', 'table_number')},
        ),
        migrations.AddIndex(
            model_name='reservation',
            index=models.Index(fields=['table', 'reservation_date'], name='first_app_r_table_i_bec81c_idx'),
        ),
        migrations.AddIndex(
            model_name='inventory',
            index=models.Index(fields=['warehouse', 'product'], name='first_app_i_warehou_20994e_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='inventory',
            unique_together={('warehouse', 'product')},
        ),
        migrations.AddIndex(
            model_name='employee',
            index=models.Index(fields=['first_name', 'last_name'], name='first_app_e_first_n_7a7cc3_idx'),
        ),
        migrations.AddConstraint(
            model_name='employee',
            constraint=models.CheckConstraint(condition=models.Q(('restaurant__isnull', True), ('warehouse__isnull', True), _connector='OR'), name='employee_single_assignment'),
        ),
    ]
