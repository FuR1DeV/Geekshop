from django.contrib.auth.decorators import login_required
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.shortcuts import get_object_or_404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db import transaction

from django.forms import inlineformset_factory
from django.utils.decorators import method_decorator

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from basketapp.models import Basket
from ordersapp.models import Order, OrderItem
from ordersapp.forms import OrderItemForm


@method_decorator(login_required, name='dispatch')
class OrderList(ListView):
    model = Order
    extra_context = {'title': 'GeekShop - состояние заказов'}

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


@method_decorator(login_required, name='dispatch')
class OrderItemsCreate(CreateView):
    model = Order
    fields = []
    success_url = reverse_lazy('order:list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'GeekShop - создание заказов'
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_items = Basket.objects.filter(user=self.request.user)
            if basket_items.exists():
                OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=basket_items.count())
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_items[num].product
                    form.initial['quantity'] = basket_items[num].quantity
                basket_items.delete()
            else:
                formset = OrderFormSet()

        data['orderitems'] = formset
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class OrderItemsUpdate(UpdateView):
    model = Order
    fields = []
    success_url = reverse_lazy('order:list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'GeekShop - добавление заказов'
        OrderFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1)

        if self.request.POST:
            data['orderitems'] = OrderFormSet(self.request.POST, instance=self.object)
        else:
            data['orderitems'] = OrderFormSet(instance=self.object)

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class OrderDelete(DeleteView):
    model = Order
    success_url = reverse_lazy('order:list')
    extra_context = {'title': 'GeekShop - удаление заказа'}


@method_decorator(login_required, name='dispatch')
class OrderRead(DetailView):
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'GeekShop - заказ/просмотр'
        return context


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()
    return HttpResponseRedirect(reverse('order:list'))


@receiver(pre_save, sender=Basket)
@receiver(pre_save, sender=Order)
def product_quantity_update_save(sender, update_fields, instance, **kwargs):
    # if 'product' in update_fields or 'quantity' in update_fields:
    if instance.pk:
        instance.product.quantity -= instance.quantity - instance.get_item(instance.pk).quantity
    else:
        instance.product.quantity -= instance.quantity
    instance.product.save()


@receiver(pre_delete, sender=Basket)
@receiver(pre_delete, sender=Order)
def product_quantity_update_delete(sender, instance, **kwargs):
    instance.product.quantity += instance.quantity
    instance.product.save()
