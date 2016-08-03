var check = -1;

$(document).ready(function () {

    /**
     * Suggestion Bar
     */
    $('#suggestion').keyup(function (e) {
        var query;
        var data = $(this).data('page');
        query = $(this).val();

        if (!query) {
            $('#artsuggest').show();
        }
        $.get('/suggest_art/', {suggestion: query, page: data}, function (data) {

            $('#artsuggest').html(data).show();
        });
    });


    /**
     * Show navbars for sort and for filter
     */
    $('#sortToggle').click(function () {
        $('#sort').slideToggle('slow');
                $('#filters').hide();
    });

    $('#filterToggle').click(function () {
            $('#filters').slideToggle('slow');
            $('#sort').hide();
    });


    /**
     * Sort by price
     */

    $('#checkpriceDesc').click(function () {
        $('#checkpriceDesc').toggleClass('active');
    });

    $('#checkpriceAsc').click(function () {
        $('#checkpriceAsc').toggleClass('active');
    });


});
