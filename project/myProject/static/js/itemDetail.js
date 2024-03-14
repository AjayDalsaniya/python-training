let reviewForm = document.querySelector('.review-rating-form');

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

    $('.changeQuantity').click(function (e) { 
        e.preventDefault();
        
        var item_id = $(this).closest('.product_data').find('.item_id').val();
        var item_qty = $(this).closest('.product_data').find('.qty-input').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: 'POST',
            url: "/update-cart",
            data: {
                'item_id':item_id,
                'item_qty':item_qty,
                csrfmiddlewaretoken:token
            },
            success: function (response) {
                // alertify.success(response.status);
            }
        });
    });
   
    $('.delete-cart-item').click(function (e) { 
        e.preventDefault();

        let confirmation = confirm("Are you sure you want to remove the item from cart?");

        if(confirmation){
            var item_id = $(this).closest('.product_data').find('.item_id').val();
            var token = $('input[name=csrfmiddlewaretoken]').val();

            $.ajax({
                method: "POST",
                url: "/delete-cart-item",
                data: {
                    'item_id':item_id,
                    csrfmiddlewaretoken:token
                },
                success: function (response) {
                    alertify.set('notifier','position', 'top-right');
                    alertify.success(response.status);
                    $('.card-data').load(location.href + " .card-data");
                }
            });
        }
        else{
            $('.card-data').load(location.href + " .card-data");
        }
    });
    
    $('#userReview-btn').click(function (e) { 
        e.preventDefault();
        reviewForm.classList.add('active');
    });
    $('#close-review-rating-form').click(function (e) { 
        e.preventDefault();
        reviewForm.classList.remove('active');
    });
});