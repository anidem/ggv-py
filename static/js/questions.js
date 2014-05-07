// questions.js
jQuery(function($) {
	$("#submitter").click(function () {
		var worksheet = "2";
		// Check the text areas
		var noval = 0;
		$("form textarea").each(function() {
			if(this.value == "") noval++;
		});
		
		if (noval > 0) return alert("Please answer all questions. Thanks!");

		// Check the multiple choices
		var radios = {};
		$("form input:radio").each(function() {	radios[this.name] = true; });
		for(i in radios) {
			if (! $(":radio[name="+i+"]:checked").length)
			     return alert("Please answer all questions. Thanks!");
		}	

		var postdata = new Array();
		postdata = $("#worksheet_form").serializeArray();
		
		// Send it off!
		console.log(SITE_ROOT+"/submitprep");
		$.post("/ggv/worksheet/"+worksheet, postdata, function(data) {
			// $("#surveycontent").remove();
			// $("#ajaxmsg").html(data);
		});	
	});


	$(document).ready(function() {});
});

