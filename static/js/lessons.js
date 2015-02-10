// lessons.js
jQuery(function($) {
    $( ".bookmarkform" ).submit(function( event ) {
        event.preventDefault();
        $.ajax({
            url : "/ggv/bookmark/add/",
            type : "POST",
            data : $(this).serializeArray(),
            dataType : "json",

            // handle a successful response
            success : function(json) {   
                // $('#notes').append('<dt><small>' + json.creator + '</small><small style="float: right"> ' + json.modified + '</small></dt><dd class="well"> ' + json.text + '</dd>');
                // $('#noteform').trigger("reset");
                console.log('success');
            },

            // handle a non-successful response
            error : function(xhr, errmsg, err) {
                console.log(xhr.status + ": " + err ); // provide a bit more info about the error to the console
            }
        });        
    });

    $( ".bookmarkform" ).change(function(event) {
        event.preventDefault();
        var flagger = $(this); // The bookmark form that has changed.
        bkmark = flagger.attr('data-target');
        bkmarktype = flagger.find("input:checked").val();
        
        if (bkmark && bkmarktype === 'none') {
            action_handler = "/ggv/bookmark/delete/" + bkmark + "/";
        } else if (bkmark && bkmarktype !== 'none') {
            action_handler = "/ggv/bookmark/update/" + bkmark + "/";
        } else if (bkmarktype !== 'none') {
            action_handler = "/ggv/bookmark/add/"
        } else {
            $( flagger.attr('data-panel') ).collapse('hide');
            return;
        }        

        console.log("ACTION: " + action_handler);
        console.log(flagger.serializeArray());

        $.ajax({
            url : action_handler,
            type : "POST",
            data : flagger.serializeArray(),
            dataType : "json",

            // handle a successful response
            success : function(json) {
                flagbtn = $( flagger.attr('data-update') );
                flagpnl = $( flagger.attr('data-panel') );
                if(json.bookmark_id) { 
                    flagger.attr('data-target', json.bookmark_id);
                    flagbtn.find('i.flagger').addClass('bkset');
                    flagbtn.find('span').html(json.mark_type);
                    
                }
                if(json.deleted) {
                    flagger.attr('data-target', '');
                    flagbtn.find('i.flagger').removeClass('bkset');
                    flagbtn.find('span').html('');
                }
                flagpnl.collapse('hide');
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
