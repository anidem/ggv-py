// questions.js
jQuery(function($) {
	$("#submit_sheet").click(function () {
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

	/*Set up for ajax post methods and django cross site request forgery (CSRF) protection
	 SEE: https://docs.djangoproject.com/en/1.4/ref/contrib/csrf/
	*/
	function getCookie(name) {
    	var cookieValue = null;
	    if (document.cookie && document.cookie != '') {
	        var cookies = document.cookie.split(';');
	        for (var i = 0; i < cookies.length; i++) {
	            var cookie = jQuery.trim(cookies[i]);
	            // Does this cookie string begin with the name we want?
	            if (cookie.substring(0, name.length + 1) == (name + '=')) {
	                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                break;
	            }
	        }
	    }
    	return cookieValue;
	}
	var csrftoken = getCookie('csrftoken');
	
	function csrfSafeMethod(method) {
	    // these HTTP methods do not require CSRF protection
	    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	
	$.ajaxSetup({
	    crossDomain: false, // obviates need for sameOrigin test
	    beforeSend: function(xhr, settings) {
	        if (!csrfSafeMethod(settings.type)) {
	            xhr.setRequestHeader("X-CSRFToken", csrftoken);
	        }
	    }
	});
	/*END csrf protection setup for ajax post methods*/

	$(document).ready(function() {

	});
});
