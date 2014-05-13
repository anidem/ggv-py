// questions.js
jQuery(function($) {
	$("div.radio").click(function () {
		$(this).parent().removeClass("required");
	});

	$("#submit_sheet").click(function () {
		var worksheet = $("#worksheet").val();
		var postdata = $("#worksheet_form").serializeArray();
		$.post("/ggv/worksheet/"+worksheet, postdata, function(data) {
			$("div.required label:first-child").css("background-color", "yellow");
			for(i in data) {
				$("#feedback").html(data[i]);
			}
		});	
	});


	$(document).ready(function() {});
});
