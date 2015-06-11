// lessons.js
jQuery(function($) {

    // TODO: Add isotope filtering.

    $( ".bookmarkform" ).change(function(event) {
        event.preventDefault();
        var flagger = $(this); // The bookmark form that has changed.
        var bkmark = flagger.find('.bktarget').val();
        var bkmarktype = flagger.find("input:checked").val();

        if(!bkmark) {
            // no previous bookmark, we're going to add one
            action_handler = "/ggv/bookmark/add/";
        } else if(bkmarktype === "none") {
            // previous bookmark set, we're going to clear it
            action_handler = "/ggv/bookmark/delete/" + bkmark + "/";
        } else {
            // previous bookmark set, we're going to change it
            action_handler = "/ggv/bookmark/update/" + bkmark + "/";
        }

        $.ajax({
            url : action_handler,
            type : "POST",
            data : flagger.serializeArray(),
            dataType : "json",

            // handle a successful response
            success : function(json) {
                flagbtn = $( flagger.attr('data-update') );
                flagpnl = $( flagger.attr('data-panel') );
                flagged = flagbtn.find('i.bookmarker');
                if(json.bookmark_id) {
                    // console.log("bk set: "+json.mark_type);
                    flagger.find('.bktarget').val(json.bookmark_id);
                    flagger.find('.bklabel').val(json.mark_type);
                    flagged.removeClass('fa-star-o');
                    flagged.addClass('fa-star');
                    flagbtn.find('.bookmark_label').html(json.mark_type);
                }
                if(json.deleted) {
                    // console.log("bk cleared");
                    flagger.find('.bktarget').val('');
                    flagger.find('.bklabel').val(' ');
                    flagged.removeClass('fa-star');
                    flagged.addClass('fa-star-o');
                    flagbtn.find('.bookmark_label').html('');
                }
                flagpnl.collapse('hide');
            },

            // handle a non-successful response
            error : function(xhr, json) {
                console.log(xhr.status + "Bookmarker error: " + json );
            }
        });

    });

    $(window).load(function() {
        $( ".bookmarkpanel" ).each(function() {
            // read the values from form's hiddent input
            var bookmark = $(this).find(".bktarget").val();
            var bookmark_display = $(this).find(".bklabel").val();
            var bookmark_star = $(this).find('i');

            $(this).find('.bookmark_label').html(bookmark_display);
            if(bookmark) {
                $(bookmark_star).removeClass('fa-star-o');
                $(bookmark_star).addClass('fa-star');
            } else {
                $(bookmark_star).removeClass('fa-star');
                $(bookmark_star).addClass('fa-star-o');
            }
        });


    });
});
