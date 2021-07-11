window.onload = function () {
    let _quantity, _price, orderitem_num, delta_quantity, orderitem_quantity, delta_cost;
    let quantity_arr = [];
    let price_arr = [];

    let total_forms = parseInt($('input[name=orderitems-TOTAL_FORMS]').val());

    let order_total_quantity = parseInt($('.order_total_quantity').text()) || 0;
    let order_total_price = parseFloat($('.order_total_cost').text()) || 0;

    for (let i = 0; i < total_forms; i++) {
        _quantity = parseInt($("input[name=orderitems-" + i + "-quantity]").val());
        _price = parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.'));

        quantity_arr[i] = _quantity;
        if (_price) {
            price_arr[i] = _price;
        } else {
            price_arr[i] = 0;
        }
    }

    $('.order_form').on('change', 'input[type=number]', function () {
        let target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
        if (price_arr[orderitem_num]) {
            orderitem_quantity = parseInt(target.value);
            delta_quantity = orderitem_quantity - quantity_arr[orderitem_num];
            quantity_arr[orderitem_num] = orderitem_quantity;
            orderSummoryUpdate(price_arr[orderitem_num], delta_quantity);


        }
    });

    $('.order_form').on('change', 'input[type=checkbox]', function () {
        let target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-DELETE', ''));
        if (target.checked) {
            delta_quantity = -quantity_arr[orderitem_num];
        } else {
            delta_quantity = quantity_arr[orderitem_num];
        }
        orderSummoryUpdate(price_arr[orderitem_num], delta_quantity);

    });

    $('.formset_row').formset({
        addText: "Добавить продукт",
        deleteText: 'Удалить',
        prefix: 'orderitems',
        remove: deleteOrderItem,
    });

    $('.order_form').on('change', 'select', function (event) {
        orderitem_num = parseInt(event.target.name.replace('orderitems-', '').replace('-product', ''));
        console.log(event.target.value)
        $.ajax({
            url: "/order/update/orderitem/" + event.target.value,
            success: function (data) {
                 price_arr[orderitem_num] = parseFloat(data.price);
                var currentTr = $('.order_form').find('tr:eq(' + (orderitem_num + 1) + ')');
                currentTr.find('td:eq(2)').text(data.price);
                },
            });
        calcOrderSumm();
    });

    function calcOrderSumm(){
        order_total_price = 0;

        for (let i = 0; i < total_forms; i++) {
            order_total_price += quantity_arr[i] * price_arr[i];
        }
        console.log(order_total_price)
        $('.order_total_cost').text(order_total_price);
    }

    function deleteOrderItem(row) {
        let target_name = row[0].querySelector('input[type=number]').name;
        orderitem_num = parseInt(target_name.replace('orderitems-', '').replace('-quantity', ''));

        delta_quantity = -quantity_arr[orderitem_num];
        orderSummoryUpdate(price_arr[orderitem_num], delta_quantity);
    }


    function orderSummoryUpdate(orderitem_price, delta_quantity) {
        delta_cost = price_arr[orderitem_num] * delta_quantity;
        order_total_price = Number((order_total_price + delta_cost).toFixed(2));
        order_total_quantity = order_total_quantity + delta_quantity;

        $('.order_total_quantity').text(order_total_quantity);
        $('.order_total_cost').text(order_total_price);
    }
};
