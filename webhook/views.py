import json, ast
import requests
import time

from django.http import HttpResponse
from django.shortcuts import redirect

CONNECTION_ERROR = 'Lo siento, hemos tenido problemas al solicitar '

WORDPRESS_API = 'wp-json/wp/v2/'
POSTS = 'posts'

CALL = 'https://www.ull.es/portal/convocatorias/'
CALL_API = CALL + WORDPRESS_API + 'convocatorias'

NEWS = 'https://www.ull.es/portal/noticias/'
NEWS_API = NEWS + WORDPRESS_API + POSTS

EVENTS = 'https://www.ull.es/portal/agenda'
EVENTS_API = EVENTS + '/wp-json/tribe_events/v2/events/'

TOTAL_PAGE = 2

def getData(action, request):
    return {
        'showNews': showNews(request),
        'showCalls': showCalls(request),
        'showEvents': showEvents(request),
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
    
def verifyTheContextAttribute(contexts, attribute):
    try:
        contexts['parameters'][attribute]
    except KeyError:
        contexts['parameters'][attribute] = ""
    
def getBodyContext(body):
    contexts = body['result']['contexts'][0]
    
    verifyTheContextAttribute(contexts, 'numberNews')
    verifyTheContextAttribute(contexts, 'numberCalls')
    verifyTheContextAttribute(contexts, 'numberEvents')
    verifyTheContextAttribute(contexts, 'category')
    verifyTheContextAttribute(contexts, 'dateStart')
    verifyTheContextAttribute(contexts, 'dateEnd')
    
    return contexts
    
def showNews(request):
    INTRO = "Estas son las noticias disponibles:<br>"
    
    body = bodyToJSON(request.body)
    contexts = getBodyContext(body)
    
    page = TOTAL_PAGE - contexts['lifespan']
    number = contexts['parameters']['numberNews']

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
    number = contexts['parameters']['numberCalls']

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
    
def showEvents(request):
    INTRO = "Estos son los eventos disponibles:<br>"
    
    body = bodyToJSON(request.body)
    contexts = getBodyContext(body)
    
    number = contexts['parameters']['numberEvents']
    category = contexts['parameters']['category']
    dateStart = contexts['parameters']['dateStart']
    dateEnd = contexts['parameters']['dateEnd']
    
    if(dateStart == ""):
        dateStart = time.strftime("%Y-%m-%d")

    url = EVENTS_API + category + '/' + dateStart + '/'
    
    if (dateEnd != ""):
        url += dateEnd
    else: 
        url += str(number)
    
    response = requests.get(url)
    
    if response.status_code == requests.codes.ok:
        results = response.json()
        
        titleEvents = "<ul>";
        for value in results:
            titleEvents += "<li><a target='_blank' href='" + value['permalink'] + "'>" + value['post_title'] + "</a></li><br>"
        titleEvents += "</ul>"
        
        responseText = INTRO + titleEvents + 'Quieres mostrar los siguientes eventos?'
            
        return createResponseData(responseText)
        
    return createResponseData(CONNECTION_ERROR + ' los eventos.')

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