from django import forms
from . import validators
from .models import Employee, Restaurant, Warehouse


class FirstForm(forms.Form):
    name = forms.CharField(empty_value="Введите имя", min_length=1, label='Name',
                           error_messages={'min_length': 'Введите хотя бы 1 символ'})
    email = forms.EmailField(empty_value="Введите почту", min_length=1, label='Email',
                             validators=(validators.valid_email,),
                             error_messages={'min_length': 'Введите хотя бы 1 символ'})


class EmployeeForm(forms.ModelForm):
    restaurant = forms.ModelChoiceField(empty_label="Выберите ресторан", queryset=Restaurant.objects.all(),
                                        required=False)
    warehouse = forms.ModelChoiceField(empty_label="Выберите склад", queryset=Warehouse.objects.all(),
                                       required=False)

    class Meta:
        model = Employee
        exclude = ['slug', 'hire_date']
