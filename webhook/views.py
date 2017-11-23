import json, ast
import requests

from django.http import HttpResponse
from django.shortcuts import redirect

CONNECTION_ERROR = 'Lo siento, hemos tenido problemas al solicitar '

WORPRESS_API = 'wp-json/wp/v2/'

NEWS = 'https://www.ull.es/portal/noticias/'
NEWS_API = NEWS + WORPRESS_API + 'posts'

TOTAL_PAGE = 2

def getData(action, request):
    return {
        'showNews': showNews(request),
    }[action]
    
def createList(values):
    listText = "<ul>";
    
    for value in values:
        listText += "<li><a target='_blank' href='" + value['link'] + "'>" + value['title']['rendered'] + "</a></li><br>"
    listText += "</ul>"
    
    return listText

def showNews(request):
    INTRO = "Estas son las noticias disponibles:<br>"
    
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    
    contexts = body['result']['contexts'][0]
    
    page = TOTAL_PAGE - contexts['lifespan']
    number = contexts['parameters']['number']

    response_data = {}
    params = "?page=" + str(page)
    if(str(number).isdigit()):
        params += "&per_page=" + str(number)
    
    url = NEWS_API + params
    
    response = requests.get(url)
    
    if response.status_code == requests.codes.ok:
        results = response.json()

        titleNews = createList(results)
        
        responseText = INTRO + titleNews + 'Quieres mostrar las siguientes noticias?'
            
        response_data['speech'] = responseText
        response_data['displayText'] = responseText
        
    else: 
        error = CONNECTION_ERROR + ' las noticias.'
        response_data['speech'] =  error
        response_data['displayText'] = error
    
    return response_data

def index(request):
    return HttpResponse("Webhook to NewsAgent.")
    
def main(request):
    if(len(request.body) == 0):
        return redirect(index)
        
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    
    data = getData(body['result']['action'], request)
    
    return HttpResponse(
        json.dumps(data),
        content_type="application/json"
    )