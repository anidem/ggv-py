// questions.js
jQuery(function($) {
	// $("#submit_sheet").click(function () {
	// 	var worksheet = $("#worksheet").val();
	// 	var postdata = $("#worksheet_form").serializeArray();
	// 	$.post("/ggv/worksheet/"+worksheet, postdata, function(data) {
	// 		if (data.errors) {
	// 			$("#feedback").html(data.errors);

	// 		} else {
	// 			$("#feedback").html(data.messages);
	// 			$(".glyphicon").css("display", "inline");
	// 		}
	// 	});	
	// });

    $( "#noteform" ).submit(function( event ) {
        event.preventDefault();
        $.ajax({
            url : "/ggv/note/add/",
            type : "POST",
            data : $( "#noteform" ).serializeArray(),
            dataType : "json",

            // handle a successful response
            success : function(json) {
                $('#notes').append('<div class="message"><span class="ts">' + json.modified + '</span> ' + json.creator + ': ' + json.text + '</div>');
                $('#noteform').trigger("reset");
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
