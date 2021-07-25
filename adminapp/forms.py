from django import forms
from authapp.forms import UserRegisterForm, UserProfileForm
from authapp.models import User
from mainapp.models import ProductCategory, Product


class UserAdminRegisterForm(UserRegisterForm):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'image', 'first_name', 'last_name', 'password1', 'password2')


class UserAdminProfileForm(UserProfileForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control py-4'}))


class AdminProductCategoryCreateForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control py-4'}), required=False)

    class Meta:
        model = ProductCategory
        fields = ('name', 'description')


class AdminProductCreateForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control py-4'}))
    price = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control py-4'}))
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control py-4'}))
    category = forms.ModelChoiceField(queryset=ProductCategory.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-select form-control'}))

    class Meta:
        model = Product
        fields = ('name', 'description', 'image', 'price', 'quantity', 'category')
