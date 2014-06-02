// questions.js
jQuery(function($) {
	$("#worksheet_form").submit(function () {
		var worksheet = $("#worksheet").val();
		var postdata = $("#worksheet_form").serializeArray();
		$.post("/ggv/worksheet/"+worksheet, postdata, function(data) {
			if (data.errors) {
				$("#feedback").html(data.errors);

			} else {
				$("#feedback").html(data.messages);
				$(".glyphicon").css("display", "inline");
			}
		});	
	});

	$(document).ready(function() {

	});
});
