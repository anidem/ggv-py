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

    $( ".bookmarkform" ).submit(function( event ) {
        event.preventDefault();
        $.ajax({
            url : "/ggv/bookmark/add/",
            type : "POST",
            data : $(this).serializeArray(),
            dataType : "json",

            // handle a successful response
            success : function(json) {   
                console.log('success');
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
