// base.js
jQuery(function($) {
    var $container = $('#container_0').isotope({
        getSortData: {
            login: '.login',
            recent: '.recent',
            firstname: '.firstname',
            lastname: '.lastname',
            username: '.username'
        },
        sortBy: '.firstname'
    });

    // sort items on button click
    $('#sorts').on( 'click', 'button', function() {
        var sortByValue = $(this).attr('data-sort-by');
        var order = "";
        if ($(this).attr("data-order")==="asc") {
            order = true;
            $(this).attr("data-order", "");

        } else {
            order = false;
            $(this).attr("data-order", "asc");
        }

        console.log(order);
        $container.isotope({
            sortBy: sortByValue,
            sortAscending: order
        });
    });

    $(document).ready(function() {

    });
});
