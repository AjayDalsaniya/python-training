$(document).ready(function () {
    $('.increment-btn').click(function (e) { 
        e.preventDefault();
        
        var inc_value = $(this).closest('.product_data').find('.qty-input').val();
        var value = parseInt(inc_value,10);

        value = isNaN(value) ? 0 : value;

        if(value < 10){
            value++;
            $(this).closest('.product_data').find('.qty-input').val(value);
        }
    });
    $('.decrement-btn').click(function (e) { 
        e.preventDefault();
        
        var dec_value = $(this).closest('.product_data').find('.qty-input').val();
        var value = parseInt(dec_value,10);
        value = isNaN(value) ? 0 : value;

        if(value > 1){
            value--;
            $(this).closest('.product_data').find('.qty-input').val(value);
        }
    });
    $('.addToCartBtn').click(function (e) { 
        e.preventDefault();
        
        var item_id = $(this).closest('.product_data').find('.item_id').val();
        var item_qty = $(this).closest('.product_data').find('.qty-input').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: 'POST',
            url: "/add-to-cart",
            data: {
                'item_id':item_id,
                'item_qty':item_qty,
                csrfmiddlewaretoken:token
            },
            success: function (response) {
                alertify.set('notifier','position', 'top-right');
                if (response.status) {
                    alertify.success(response.status);
                }else{
                    alertify.error(response.data);
                }
            }
        });
    });
});