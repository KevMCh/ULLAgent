var baseUrl = "https://api.api.ai/v1/";

$(document).ready(function() {
    $("#input").keypress(function(event) {
        if (event.which == 13) {
        	
        	var userMessage = $("#input").val();

            setUserMessage(userMessage);
            send(userMessage);
            
            event.preventDefault();
        }
	});
});

function setUserMessage(text){
	$("#conversation").append("<div class='container'>\
		<img src='' alt='User' style='width:100%;'>\
		<p>" + text + "</p>\
		</div>");
    
    $("#input").val("");
}

function setBotMessage(text) {
	$("#conversation").append("<div class='container darker'>\
		<img src='' alt='Avatar' class='right' style='width:100%;'>\
		<p>" + text + "</p>\
		</div>");
}

function send(text) {
	$.ajax({
		type: "POST",
		url: baseUrl + "query?v=20150910",
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		headers: {
			"Authorization": "Bearer " + ACCESSTOKEN
		},

		data: JSON.stringify({ query: text, lang: "en", sessionId: "somerandomthing" }),
		success: function(data) {
			console.log(data)
			setBotMessage(data.result.fulfillment.messages[0].speech);
			$("#conversation").animate({ scrollTop: $('#conversation')[0].scrollHeight}, 0);
		},
		
		error: function(error) {
			console.log(error);
		}
	});
}