var baseUrl = "https://api.api.ai/v1/";

$(document).ready(function() {
    $("#input").keypress(function(event) {
        if (event.which == 13) {
        	var userMessage = $("#input").val();
			sendUserMessage(userMessage);
            
            event.preventDefault();
        }
	});
	
	$('#buttonBot').click(function() {
		$(this).hide();
		$('#chatbox').show();
	});
	
	$('#minimize').click(function() {
		$('#chatbox').hide();
		$('#buttonBot').show();
	});
	
	send("Hola");
});

function sendUserMessage(text) {
	setUserMessage(text);
	send(text);
}

function setUserMessage(text) {
	$("#conversation").append("<div class='sended-message message-own'>\
		<div align=left class='content'>" +
			text +
		"</div>\
	</div>");
	
    $("#input").val("");
    $("#conversation").animate({ scrollTop: $('#conversation')[0].scrollHeight}, 0);
}

function setBotMessage(text) {
	$("#conversation").append("<div class='sended-message message-bot'>\
		<div align=left class='content'>" + 
			text +
		"</div>\
	</div>");

	$("#conversation").animate({ scrollTop: $('#conversation')[0].scrollHeight}, 0);
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

			var messages = data.result.fulfillment.messages;
			for (i = 0; i < messages.length; i++) {
    			setBotMessage(messages[i].speech);
			}
		},
		
		error: function(error) {
			console.log(error);
		}
	});
}