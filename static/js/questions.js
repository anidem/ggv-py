// questions.js
jQuery(function($) {
    $( "#noteform" ).submit(function( event ) {
        event.preventDefault();
        $.ajax({
            url : "/ggv/note/add/",
            type : "POST",
            data : $( "#noteform" ).serializeArray(),
            dataType : "json",

            // handle a successful response
            success : function(json) {
                $('#notes').append('<dt><small>' + json.creator + '</small><small style="float: right"> ' + json.modified + '</small></dt><dd class="well"> ' + json.text + '</dd>');
                $('#noteform').trigger("reset");
            },

            // handle a non-successful response
            error : function(xhr, errmsg, err) {
                console.log(xhr.status + ": " + err ); // provide a bit more info about the error to the console
            }
        });
	});

    $( ".flagger" ).click(function( event ) {
        var flagger = $(this);
        form = $( flagger.attr('data-form') );
        bkmark = flagger.attr('data-target');
        flagger.toggleClass('bkset');

        if (flagger.hasClass('bkset'))
            action_handler = "/ggv/bookmark/add/";
        else
            action_handler = "/ggv/bookmark/delete/" + bkmark + "/";

        $.ajax({
            url : action_handler,
            type : "POST",
            data : form.serializeArray(),
            dataType : "json",

            // handle a successful response
            success : function(json) {
                if(json.bookmark_id) {
                    flagger.attr('data-target', json.bookmark_id);
                }
                if(json.deleted) {
                    flagger.attr('data-target', '');
                }
                console.log(json);
            },

            // handle a non-successful response
            error : function(xhr, errmsg, err) {
                console.log(xhr.status + ": " + err ); // provide a bit more info about the error to the console
            }
        });

    });

	$(document).ready(function() {

	});
});
