// questions.js
jQuery(function($) {
	$("#submit_sheet").click(function () {
		var worksheet = $("#worksheet").val();
		var postdata = $("#worksheet_form").serializeArray();
		console.log(worksheet);
		// Send it off!
		$.post("/ggv/worksheet/"+worksheet, postdata, function(data) {
			$("#feedback").html(data['success'] + " " + data["error_msg"]);
		});	
	});


	$(document).ready(function() {});
});