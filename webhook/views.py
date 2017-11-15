import json

from django.http import HttpResponse

def index(request):
    return HttpResponse("Webhook to NewsAgent.")
    
def news(request):
    response_data = {}
    response_data['speech'] = 'This is the news.'
    response_data['displayText'] = 'This is the news'

    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )