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
      console.log('clicked');
      var sortByValue = $(this).attr('data-sort-by');
      $container.isotope({ sortBy: sortByValue });
    });

    $(document).ready(function() {

    });
});
