$(document).ready(function(){


        $("input[name='sort']").click(function(){


            var s = window.location.href;
            s.split("/");

            var prevValue = $(this).attr('previousValue');
            var name = $(this).attr('name');

            if (prevValue == 'checked') {
                $(this).removeAttr('checked');
                $(this).attr('previousValue', false);
            } else {
                $("input[name="+name+"]:radio").attr('previousValue', false);
                $(this).attr('previousValue', 'checked');
            }


            var sort_type = $("input[name='sort']:checked").val();
            //if(sort_type) {

            /**
             * Get the checked categories
             */
            var checked_cats = [];
            $(this).find("input[type=checkbox]:checked").each(function () {
                checked_cats.push($(this).attr('value'));
            });

                /**
                 * Get the price slider values
                 */

            var filter = $('#filter');
            var slider_3 = filter.siblings('#slider-3');
            var fv = slider_3.slider("values", 0);
            var sv = slider_3.slider("values", 1);

                /**
                 * GEt the checked types
                 * @type {Array}
                 */
            var checked_types = [];
            $('#type-list').find("input[type=checkbox]:checked").each(function () {
                checked_types.push($(this).attr('value'));
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
                        'sort_type': sort_type,
                        'view_type': view_type,
                        'search': s
                    },
                    success: function (data) {
                        $('#filtering-template-container').html(data).show();
                    }
            });
    });
});
