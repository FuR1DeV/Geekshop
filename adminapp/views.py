from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.db import connection
from django.db.models import F

from authapp.models import User
from mainapp.models import ProductCategory, Product
from adminapp.forms import UserAdminRegisterForm, UserAdminProfileForm, AdminProductCategoryCreateForm, \
    AdminProductCreateForm


@user_passes_test(lambda u: u.is_superuser)
def index(request):
    return render(request, 'adminapp/admin.html')


# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_read(request):
#     context = {'users': User.objects.all()}
#     return render(request, 'adminapp/admin-users-read.html', context)


class UserListView(ListView):
    model = User
    template_name = 'adminapp/admin-users-read.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserListView, self).dispatch(request, *args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_create(request):
#     if request.method == 'POST':
#         form = UserAdminRegisterForm(data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admin_staff:admin_users_read'))
#     else:
#         form = UserAdminRegisterForm()
#     context = {'form': form}
#     return render(request, 'adminapp/admin-users-create.html', context)


class UserCreateView(CreateView):
    model = User
    template_name = 'adminapp/admin-users-create.html'
    form_class = UserAdminRegisterForm
    success_url = reverse_lazy('admin_staff:admin_users_read')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserCreateView, self).dispatch(request, *args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_update(request, user_id):
#     selected_user = User.objects.get(id=user_id)
#     if request.method == 'POST':
#         form = UserAdminProfileForm(data=request.POST, files=request.FILES, instance=selected_user)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admin_staff:admin_users_read'))
#     else:
#         form = UserAdminProfileForm(instance=selected_user)
#     context = {
#         'form': form,
#         'selected_user': selected_user
#     }
#     return render(request, 'adminapp/admin-users-update-delete.html', context)


class UserUpdateView(UpdateView):
    model = User
    template_name = 'adminapp/admin-users-update-delete.html'
    success_url = reverse_lazy('admin_staff:admin_users_read')
    form_class = UserAdminProfileForm

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserUpdateView, self).dispatch(request, *args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_remove(request, user_id):
#     user = User.objects.get(id=user_id)
#     user.is_active = False
#     user.save()
#     return HttpResponseRedirect(reverse('admin_staff:admin_users_read'))


class UserDeleteView(DeleteView):
    model = User
    template_name = 'adminapp/admin-users-update-delete.html'
    success_url = reverse_lazy('admin_staff:admin_users_read')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(success_url)

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserDeleteView, self).dispatch(request, *args, **kwargs)


@user_passes_test(lambda u: u.is_superuser)
def admin_users_restore(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()
    return HttpResponseRedirect(reverse('admin_staff:admin_users_read'))


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class CategoryListView(ListView):
    model = ProductCategory
    template_name = 'adminapp/admin-categories-read.html'


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class CategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/admin-categories-create.html'
    form_class = AdminProductCategoryCreateForm
    success_url = reverse_lazy('admin_staff:admin_categories_read')


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]

@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class CategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/admin-categories-update-delete.html'
    success_url = reverse_lazy('admin_staff:admin_categories_read')
    form_class = AdminProductCategoryCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_category'] = ProductCategory.objects.get(id=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.product_set.update(price=F('price') * (1 - discount / 100))
                db_profile_by_type(self.__class__, 'UPDATE', connection.queries)

        return super().form_valid(form)

@user_passes_test(lambda u: u.is_superuser)
def admin_categories_remove(request, category_id):
    category = ProductCategory.objects.get(id=category_id)
    category.delete()
    return HttpResponseRedirect(reverse('admin_staff:admin_categories_read'))


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductListView(ListView):
    model = Product
    template_name = 'adminapp/admin-products-read.html'


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    template_name = 'adminapp/admin-products-create.html'
    form_class = AdminProductCreateForm
    success_url = reverse_lazy('admin_staff:admin_products_read')


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'adminapp/admin-products-update-delete.html'
    success_url = reverse_lazy('admin_staff:admin_products_read')
    form_class = AdminProductCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_product'] = Product.objects.get(id=self.kwargs['pk'])
        return context


@user_passes_test(lambda u: u.is_superuser)
def admin_products_remove(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    return HttpResponseRedirect(reverse('admin_staff:admin_products_read'))

