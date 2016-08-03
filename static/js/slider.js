$(function () {
    var minPrice = 0, maxPrice  = Math.abs($('#max-price').val());
    $("#slider-3").slider({
        range: true,
        min: minPrice,
        max: maxPrice,
        values: [minPrice, maxPrice],
        slide: function (event, ui) {
            $("#price").val("£" + ui.values[0] + " - £" + ui.values[1]);
        },

        // when the user stopped changing the slider

        stop: function (event, ui) {
            var fv = $("#slider-3").slider("values", 0);
            var sv = $("#slider-3").slider("values", 1);

            var s = window.location.href;
            s.split("/");

            var slide_3 = $('#slider-3');
            var filter_div = slide_3.siblings('#filter');
            var categories_list = filter_div.find('#category-list');
            var checked_cats = [];
            categories_list.find("input[type=checkbox]:checked").each(function () {
                checked_cats.push($(this).attr('value'));
            });
             var checked_types = [];
            $('#type-list').find("input[type=checkbox]:checked").each(function(){
            checked_types.push($(this).attr('value'));
            });

            var sorts = [];
            $('#sort').find("input[type=radio]:checked").each(function(){
            sorts.push($(this).attr('value'));
            });

                    var view_type = $("input[name='view']:checked").val();


            $.ajax({
                url: "/apply_filtering/",
                traditional: true,
                data: {
                    'small_value': fv,
                    'large_value': sv,
                    'checked_cats': checked_cats,
                    'checked_types': checked_types,
                    'sort_type': sorts,
                    'view_type': view_type,
                    'search': s
                },
                success: function(data){
                    $('#filtering-template-container').html(data).show;
                }
            });
        }


    });

    $("#price").val("£" + $("#slider-3").slider("values", 0) +
        " - £" + $("#slider-3").slider("values", 1));


});