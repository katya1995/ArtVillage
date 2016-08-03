$(document).ready(function () {


    var delivery_type = $("input[name='delivery']:checked").val();
    $('#store-delivery').slideToggle('slow');
    $('#home-delivery').hide();

    $('#delivery-store').click(function () {

        $('#store-delivery').slideToggle('slow');
        $('#home-delivery').hide();
        delivery_type = "store";
        var csrftoken = Cookies.get('csrftoken');


        $.post('/cart/', {'delivery_type': delivery_type, csrfmiddlewaretoken: csrftoken},
            function (data) {
                $("#cart-details").html(data);
            });
    });

    $('#delivery-home').click(function () {
        $('#home-delivery').slideToggle('slow');
        $('#store-delivery').hide();
        delivery_type = "home";
        var csrftoken = Cookies.get('csrftoken');


        $.post('/cart/', {'delivery_type': delivery_type, csrfmiddlewaretoken: csrftoken},
            function (data) {
                $("#cart-details").html(data);
            });
    });


});