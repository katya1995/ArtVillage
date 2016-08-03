$(document).ready(function() {

    $("input[name='view']").click(function () {
        var view_type = $("input[name='view']:checked").val();
        $.ajax({
            type: "GET",
            traditional: true,
            url: 'index',
            data: {
                'view_type': view_type
            },
            success: function (data) {
                $('#filtering-template-container').html(data).show();
            }
        });
    });
});