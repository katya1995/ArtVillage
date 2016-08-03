$(document).ready(function(){

        $("input[name='view']").click(function(){

        /*
            Get the checked categories plus other relevant information to remain state:
             * the price range
             * type
         */

        var s = window.location.href;
        s.split("/");

        var checked_types = [];
        $('#type-list').find("input[type=checkbox]:checked").each(function(){
            checked_types.push($(this).attr('value'));
        });

          var filter = $('#filter');
            var slider_3 = filter.siblings('#slider-3');
            var fv = slider_3.slider("values", 0);
            var sv = slider_3.slider("values", 1);


        //var type_list = filter.siblings('#type-list');
        var checked_cats = [];
        $('#category-list').find("input[type=checkbox]:checked").each(function(){
            checked_cats.push($(this).attr('value'));
        });


        var sorts = [];
            $('#sort').find("input[type=radio]:checked").each(function(){
                sorts.push($(this).attr('value'));
            });

        var view_type = $("input[name='view']:checked").val();

        /* Send the ajax request */
        $.ajax({
            type: "GET",
            traditional: true,
            url: '/apply_filtering/',
            data: {
                'small_value': fv,
                'large_value': sv,
                'checked_cats': checked_cats,
                'checked_types': checked_types,
                'sort_type': sorts,
                'view_type':view_type,
                'search': s
            },
            success: function(data){
                $('#filtering-template-container').html(data).show();
            }
        });
    });
});



