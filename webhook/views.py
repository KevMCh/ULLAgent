import json, ast
import requests

from django.http import HttpResponse
from django.shortcuts import redirect

CONNECTION_ERROR = 'Lo siento, hemos tenido problemas al solicitar '

WORDPRESS_API = 'wp-json/wp/v2/'
POSTS = 'posts'

CALL = 'https://www.ull.es/portal/convocatorias/'
CALL_API = CALL + WORDPRESS_API + 'convocatorias'

NEWS = 'https://www.ull.es/portal/noticias/'
NEWS_API = NEWS + WORDPRESS_API + POSTS

TOTAL_PAGE = 2

def getData(action, request):
    return {
        'showNews': showNews(request),
        'showCalls': showCalls(request),
    }[action]
    
def createList(values):
    listText = "<ul>";
    
    for value in values:
        listText += "<li><a target='_blank' href='" + value['link'] + "'>" + value['title']['rendered'] + "</a></li><br>"
    listText += "</ul>"
    
    return listText
    
def createResponseData(data):
    responseData = {
        'speech': data,
        'displayText': data,
    }
    return responseData
    
def bodyToJSON(requestBody):
    bodyUnicode = requestBody.decode('utf-8')
    
    return json.loads(bodyUnicode)
    
def getBodyContext(body):
    return body['result']['contexts'][0]
    
def showNews(request):
    INTRO = "Estas son las noticias disponibles:<br>"
    
    body = bodyToJSON(request.body)
    contexts = getBodyContext(body)
    
    page = TOTAL_PAGE - contexts['lifespan']
    number = contexts['parameters']['number']

    
    params = "?page=" + str(page)
    if(str(number).isdigit()):
        params += "&per_page=" + str(number)
    
    url = NEWS_API + params
    
    response = requests.get(url)
    
    if response.status_code == requests.codes.ok:
        results = response.json()

        titleNews = createList(results)
        
        responseText = INTRO + titleNews + 'Quieres mostrar las siguientes noticias?'
            
        return createResponseData(responseText)
    
    return createResponseData(CONNECTION_ERROR + ' las noticias.')

def showCalls(request):
    INTRO = "Estas son las convocatorias disponibles:<br>"
    
    body = bodyToJSON(request.body)
    contexts = getBodyContext(body)
    
    page = TOTAL_PAGE - contexts['lifespan']
    number = contexts['parameters']['number']

    params = "?page=" + str(page)
    if(str(number).isdigit()):
        params += "&per_page=" + str(number)
    
    url = CALL_API + params
    response = requests.get(url)
    
    if response.status_code == requests.codes.ok:
        results = response.json()

        titleCalls = createList(results)
        
        responseText = INTRO + titleCalls + 'Quieres mostrar las siguientes convocatorias?'
            
        return createResponseData(responseText)
        
    return createResponseData(CONNECTION_ERROR + ' las convocatorias.')

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