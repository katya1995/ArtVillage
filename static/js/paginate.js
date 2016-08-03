/**
 * Created by Owner on 16.7.2016 �..
 */

$(document).ready(function (e) {

    /* Ajax functionality to get the new page */
    $(document.body).on('click', '.new-page', function (e) {

        var s = window.location.href;
        s.split("/");

        e.preventDefault();
        var new_page = $(this).attr('value');
        var checked_cats = [];
        $('#category-list').find("input[type=checkbox]:checked").each(function () {
            checked_cats.push($(this).attr('value'));
        });

        var filter = $('#filter');
        var slider_3 = filter.siblings('#slider-3');
        var fv = slider_3.slider("values", 0);
        var sv = slider_3.slider("values", 1);


        //var type_list = filter.siblings('#type-list');
        var checked_types = [];
        $('#type-list').find("input[type=checkbox]:checked").each(function () {
            checked_types.push($(this).attr('value'));
        });

        /**
         * GET The value of the sort radiobuttons
         */

        var sorts = [];
        $('#sort').find("input[type=radio]:checked").each(function () {
            sorts.push($(this).attr('value'));
        });

        var view_type = $("input[name='view']:checked").val();


        $.ajax({
            url: '/get_new_page/',
            traditional: true,
            data: {
                'new_page': new_page,
                'checked_cats': checked_cats,
                'small_value': fv,
                'large_value': sv,
                'sort_type': sorts,
                'view_type': view_type,
                'search': s
            },
            success: function (data) {
                $('#filtering-template-container').html(data).show;
            }
        });

    });

});
