$(document).ready(function () {
    $('.payWithRazorpay').click(function (e) { 
        e.preventDefault();

        var fname = $("[name='fname']").val();
        var lname = $("[name='lname']").val();
        var email = $("[name='email']").val();
        var mobile = $("[name='mobile']").val();
        var address = $("[name='address']").val();
        var city = $('#cityd :selected').text();
        var area = $('#aread :selected').text();
        var pincode = $("[name='pincode']").val();

        if(fname == "" || lname == "" || email == "" || mobile == "" || address == "" || pincode == ""){
            swal("Error", "Please fill all details!", "error");
            return false
        }else{
            $.ajax({
                method: "GET",
                url: "/proceed-to-pay",
                success: function (response) {
                    var options = {
                        "key": "YOUR_KEY_ID",
                        "amount": "50000",
                        "currency": "INR",
                        "name": "Acme Corp",
                        "description": "Test Transaction",
                        "image": "https://example.com/your_logo",
                        "order_id": "order_9A33XWu170gUtm",
                        "handler": function (response) {
                            alert(response.razorpay_payment_id);
                            alert(response.razorpay_order_id);
                            alert(response.razorpay_signature)
                        },
                        "prefill": {
                            "name": "Gaurav Kumar",
                            "email": "gaurav@gmail.com",
                            "contact": "9023964738"
                        },
                        "notes": {
                            "address": "Razorpay Corporate Office"
                        },
                        "theme": {
                            "color": "#3399cc"
                        }
                    };
                    var rzp1 = new Razorpay(options);
                    // rzp1.on('payment.failed',function (response){
                    //     alert(response.error.code);
                    //     alert(response.error.description);
                    //     alert(response.error.source);
                    //     alert(response.error.step);
                    //     alert(response.error.reason);
                    //     alert(response.error.metadata.order_id);
                    //     alert(response.error.metadata.payment_id);
                    // });
                    rzp1.open();
                }
            });
        }
    });

    $(window).on('load', function () {
        var charges = $('.charges').text();
        var grandTotal1 = $('.grandTotal2').text();
        var gTotal = 0
        gTotal = parseInt(charges) + parseInt(grandTotal1)
        $('.grandTotal2').html(gTotal)
    });

    $('#aread').change(function (e) { 
        e.preventDefault();
        
        var charges = $('.charges').text();
        var grandTotal1 = $('.grandTotal2').text();
        var area = $(this).val();
        var gTotal
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "/change-charges",
            data: {
                'delivery_charges':charges,
                'areaname':area,
                csrfmiddlewaretoken:token
            },
            success: function (response) {
                $('.charges').html(response.status)
                gTotal = (parseInt(grandTotal1) - parseInt(charges))
                gTotal1 = gTotal + parseInt(response.status)
                $('.grandTotal2').html(gTotal1)
            }
        });
    });
});