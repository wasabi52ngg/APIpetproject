from rest_framework import viewsets, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from .models import (
    Restaurant, Table, Warehouse, Employee, Supplier, Product, Inventory,
    Menu, Dish, MenuDetail, Modifier, Customer, Reservation, Order, OrderDetail, Payment
)
from rest_framework.response import Response
from .serializers import (
    RestaurantSerializer, EmployeeSerializer, SupplierSerializer, OrderSerializer, TableSerializer, WarehouseSerializer,
    ProductSerializer, InventorySerializer, MenuSerializer, DishSerializer, MenuDetailSerializer, ModifierSerializer,
    CustomerSerializer, ReservationSerializer, OrderDetailSerializer, PaymentSerializer)


# Create your views here.
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'address']
    search_fields = ['name', 'address']
    ordering_fields = ['name', 'id']
    pagination_class = StandardResultsSetPagination


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['restaurant__slug', 'status', 'capacity']
    search_fields = ['table_number']
    ordering_fields = ['table_number', 'capacity']
    pagination_class = StandardResultsSetPagination

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def set_status(self, request, pk=None):
        table = self.get_object()
        new_status = request.data.get('status')
        if new_status not in dict(Table.STATUS_CHOICES).keys():
            return Response({'error': 'Недопустимый статус'}, status=status.HTTP_400_BAD_REQUEST)
        table.status = new_status
        table.save()
        return Response({'status': table.status}, status=status.HTTP_200_OK)


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'address']
    search_fields = ['name', 'address']
    ordering_fields = ['name', 'id']
    pagination_class = StandardResultsSetPagination


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {
        'restaurant__slug': ['exact'],
        'warehouse__slug': ['exact'],
        'role': ['exact'],
        'salary': ['exact', 'gt', 'lt', 'gte', 'lte'],
    }
    search_fields = ['first_name', 'last_name', 'role']
    ordering_fields = ['first_name', 'last_name', 'hire_date']
    pagination_class = StandardResultsSetPagination


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'email']
    search_fields = ['name', 'contact_person']
    ordering_fields = ['name', 'id']
    pagination_class = StandardResultsSetPagination


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name', 'unit', 'supplier__slug']
    search_fields = ['name']
    ordering_fields = ['name', 'id']
    pagination_class = StandardResultsSetPagination


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['warehouse__slug', 'product__slug']
    search_fields = ['product__name']
    ordering_fields = ['quantity', 'last_updated']
    pagination_class = StandardResultsSetPagination


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['restaurant__slug', 'name', 'start_date', 'end_date']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'start_date']
    pagination_class = StandardResultsSetPagination


class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category', 'base_price']
    search_fields = ['name', 'description', 'category']
    ordering_fields = ['name', 'base_price']
    pagination_class = StandardResultsSetPagination


class MenuDetailViewSet(viewsets.ModelViewSet):
    queryset = MenuDetail.objects.all()
    serializer_class = MenuDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['menu__slug', 'dish__slug', 'is_available']
    search_fields = ['dish__name']
    ordering_fields = ['price', 'is_available']
    pagination_class = StandardResultsSetPagination


class ModifierViewSet(viewsets.ModelViewSet):
    queryset = Modifier.objects.all()
    serializer_class = ModifierSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['dish__slug']
    search_fields = ['name']
    ordering_fields = ['name', 'price_change']
    pagination_class = StandardResultsSetPagination


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['email', 'phone']
    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = ['first_name', 'last_name']
    pagination_class = StandardResultsSetPagination


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['table__slug', 'customer__slug', 'reservation_date', 'status']
    search_fields = ['customer__first_name', 'customer__last_name']
    ordering_fields = ['reservation_date', 'time']
    pagination_class = StandardResultsSetPagination

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def cancel(self, request, pk=None):
        reservation = self.get_object()
        if reservation.status != Reservation.CONFIRMED:
            return Response({'error': 'Бронирование уже отменено или завершено'}, status=status.HTTP_400_BAD_REQUEST)
        reservation.status = Reservation.CANCELLED
        reservation.save()
        reservation.table.status = Table.FREE
        reservation.table.save()
        return Response({'status': reservation.status}, status=status.HTTP_200_OK)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['restaurant__slug', 'customer__slug', 'status', 'order_date']
    search_fields = ['customer__first_name', 'customer__last_name']
    ordering_fields = ['order_date', 'total_amount']
    pagination_class = StandardResultsSetPagination

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def complete(self, request, pk=None):
        order = self.get_object()
        if order.status != Order.PENDING:
            return Response({'error': 'Заказ уже завершен или отменен'}, status=status.HTTP_400_BAD_REQUEST)
        order.status = Order.COMPLETED
        order.save()
        return Response({'status': order.status}, status=status.HTTP_200_OK)


class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['order__slug', 'dish__slug']
    search_fields = ['dish__name']
    ordering_fields = ['quantity', 'price']
    pagination_class = StandardResultsSetPagination


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['order__slug', 'payment_method', 'payment_time']
    search_fields = ['transaction_id']
    ordering_fields = ['payment_time', 'amount']
    pagination_class = StandardResultsSetPagination


"""
Просто тестовые функции, но я не захотел их удалять, не обращайте на них внимание)

def first_view(request):
    response = f"<p> Привет </p>"
    get_some_employee()
    get_some_employee()
    return HttpResponse(response)


def second_view(request):
    data = {'arg': 'value'}
    return render(request, 'first_app/second.html', context=data)


def third_view(request, num):
    nums = [1, 2, 3, 4, 5]
    if num in nums:
        data = {'num_square': f'{num ** 2}'}
        return render(request, 'first_app/third.html', context=data)
    return HttpResponseNotFound("Нет такого номера в списке")


def fourth_view(request):
    if request.method == "POST":
        form = FirstForm(request.POST)
        if form.is_valid():
            return HttpResponse(
                f"<p>Ваша форма успешно принята. Ваши данные:</p>"
                f"<p>name: {form.cleaned_data['name']}</p>"
                f"<p>email: {form.cleaned_data['email']}</p>"
            )
    else:
        form = FirstForm()

    return render(request, 'first_app/fourth.html', {'form': form})


class FiveView(View):
    def get(self, request):
        form = FirstForm()
        return render(request, 'first_app/fourth.html', {'form': form})

    def post(self, request):
        form = FirstForm(request.POST)
        if form.is_valid():
            return HttpResponse(
                f"<p>Ваша форма успешно принята. Ваши данные:</p>"
                f"<p>name: {form.cleaned_data['name']}</p>"
                f"<p>email: {form.cleaned_data['email']}</p>"
            )
        return render(request, 'first_app/fourth.html', {'form': form})


class SixTemplateView(TemplateView):
    template_name = 'first_app/third.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['num_square'] = int(kwargs['num']) ** 2
        return context


class SevenListView(ListView):
    model = Employee
    template_name = 'first_app/'
    context_object_name = 'employees'
    allow_empty = True


class EmployeeCreateView(CreateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'first_app/create_employee.html'


class EmployeeDetailView(DetailView):
    model = Employee
    template_name = "first_app/detail_employee.html"
    context_object_name = 'employee'
    slug_url_kwarg = 'slug_employee'


class EmployeeUpdateView(UpdateView):
    model = Employee
    template_name = "first_app/update_employee.html"
    form_class = EmployeeForm


def get_some_employee():
    start_time = time.time()

    employee_list = cache.get('employees')

    if employee_list is None:
        employees = list(
            Employee.objects.filter(Q(salary__gt=25000) & Q(restaurant_id=3)).values('id', 'first_name', 'salary'))

        cache.set('employees', employees, 60)
        employee_list = employees

        elapsed_time = time.time() - start_time
        print(f"Данные из БД (без кэша): {elapsed_time:.4f} сек")
    else:
        elapsed_time = time.time() - start_time
        print(f"Данные из кэша: {elapsed_time:.4f} сек")

    return employee_list


class EmployeeAPIView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({'error': 'Method PUT is not allowed'})
        try:
            instance = Employee.objects.get(pk=pk)
        except:
            return Response({'error': 'Object does not exist'})
        return Response({'employy': EmployeeSerializer(instance=instance)})

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'employee': serializer.data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({'error': 'Method PUT is not allowed'})
        try:
            instance = Employee.objects.get(pk=pk)
        except:
            return Response({'error': 'Object does not exist'})

        serializer = EmployeeSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'employee': serializer.data})

    def patch(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        try:
            instance = Employee.objects.get(pk=pk)
        except:
            return Response({'error': 'Bad request'})
        serializer = EmployeeSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'employee': serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Bad request'})
        Employee.objects.delete(pk)
        return Response({'deleted post': pk})


class EmployeeRetrieveAPIView(RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeListAPIView(ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeUpdateAPIView(UpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeFULLAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeModelViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        return Response({"error": "No list"})

    @action(methods=['get'], detail=False, url_path='my-tg')
    def get_my_tg(self, request):
        return Response({'my-tg': '@mytg'})

    def get_permissions(self):
        if self.action in ('get_my_tg'):
            return [IsAuthenticated()]
        return super().get_permissions()


class EmployeeGenericViewSet(CreateModelMixin, viewsets.GenericViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
"""
