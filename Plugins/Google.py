"""
Google plugin for Superbot.
This plugin handles functionality pertaining to google such as
google search, and google weather.
"""

import urllib2, urllib
import simplejson
import lxml.html
from xml.dom import minidom

GOOGLE_AJAX_SEARCH_URL = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&"
GOOGLE_SEARCH_URL = "http://www.google.com/search?&"
GOOGLE_WEATHER_URL = "http://www.google.com/ig/api?"

HEADERS  = {'User-Agent': "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.5)"}

def _buildResponse(url, is_json=False):
    request = urllib2.Request(url, None, HEADERS)
    response = urllib2.urlopen(request)
    if is_json:
        response = simplejson.load(response)
        if not response.has_key('responseData'): return #no data pointless
        return response['responseData'] 
    return response

def google_search(params):
    """
        Returns google search results(1) for a query.
        @params (dict) contains query value
    """
    url = GOOGLE_AJAX_SEARCH_URL + urllib.urlencode(params)
    response = _buildResponse(url, is_json=True)
    if not response.has_key('results'): return #no results pointless
    results = response['results']
    result = results[0]
    searchstring = "<{C3}Google Search{}: {B}%s{} | {LINK}%s{}>" % (result['titleNoFormatting'], urllib.unquote(result['url']))
    return searchstring

def google_calc(params):
    """
        Returns google calculator results for query.
        @params (dict) contains query value
    """
    url = GOOGLE_SEARCH_URL + urllib.urlencode(params)
    response = _buildResponse(url)
    html = response.read()
    pdoc = lxml.html.fromstring(html)
    result = pdoc.body.cssselect('table.std h2.r')[0].text_content()
    return "<{C3}Google Calc{}: %s>" % result

def google_define(params, num=None):
    """
        Returns google definition for query.
        @params (dict) contains query value.
    """
    url = GOOGLE_SEARCH_URL + urllib.urlencode(params)
    response = _buildResponse(url)
    html = response.read()
    pdoc = lxml.html.fromstring(html)
    results = pdoc.body.cssselect('ul.std li')
    result = results[num].text.strip()
    link = "No link."
    try:
        link =  'http://' + pdoc.body.cssselect('ul.std li a')[num].text_content()
    except IndexError: pass
    return "<{C3}Google Define{}: %s | {LINK}%s{} [{B}%s{} of %s]>" % (result, link, num, len(results)-1)

def google_spell(params):
    """
        Returns google spelling suggestion for query.
        @params (dict) contains query value.
    """
    url = GOOGLE_SEARCH_URL + urllib.urlencode(params)
    response = _buildResponse(url)
    html = response.read()
    pdoc = lxml.html.fromstring(html)
    result = pdoc.body.cssselect('a.spell b i')[0].text_content()
    return "<{C3}Google Spell{}: {B}%s{}>" % result

def google_weather(params):
    """
        Returns weather results (str) for query.
        @params (dict) contains query and hl values
    """
    url = GOOGLE_WEATHER_URL + urllib.urlencode(params)
    response = _buildResponse(url)

    #nasty xml parsing =( this is loosely grabbed from pywapi
    response = response.read()
    dom = minidom.parseString(response)
    weather_data = {}
    weather_dom = dom.getElementsByTagName('weather')[0]
    data = {
        'forecast_information': ('city', 'forecast_date', 'current_date_time', 'unit_system' ),
        'current_conditions': ('condition', 'temp_f', 'temp_c', 'humidity', 'wind_condition', 'icon'),
    }
    for (tag, listoftags) in data.iteritems():
        tmp_conditions = {}
        for tag2 in listoftags:
            try:
                tmp_conditions[tag2] = weather_dom.getElementsByTagName(tag)[0].getElementsByTagName(tag2)[0].getAttribute('data')
            except IndexError:
                pass
        weather_data[tag] = tmp_conditions
    
    temp_c = weather_data['current_conditions']['temp_c']
    temp_f = weather_data['current_conditions']['temp_f']
    humidity = weather_data['current_conditions']['humidity']
    wind_condition = weather_data['current_conditions']['wind_condition']
    condition = weather_data['current_conditions']['condition']
    city = weather_data['forecast_information']['city']
    temp_color = 3
    humidity = float(humidity.strip('Humdity: %'))
    temp_f = float(temp_f)
    heat_index_f = round(-42.379 + 2.04901523 * temp_f + 10.14333127 * humidity + -0.22475541 * temp_f * humidity + -6.83783e-3 * temp_f**2 + -5.481717e-2 * humidity**2 + 1.22874e-3 * temp_f**2 * humidity + 8.5282e-4 * temp_f * humidity**2 + -1.99e-6 * temp_f**2 * humidity**2)
    heat_index_c = int((heat_index_f - 32) * (5 / 9))
    heat_index_f = int(heat_index_f)
    temp_f = int(temp_f)
    humidity = 'Humidity: {0}%'.format(int(humidity))
    if float(temp_f) < 45:
        temp_color = 10
    if float(temp_f) > 65:
        temp_color = 4
    weather_string = "<{C3}Google Weather{}: City: %s | Temp: {C%i}%sc/%sf{} | %s | Heat index: %sc/%sf | %s | Current Condition: %s>" % \
                                                        (city, temp_color,temp_c, temp_f, humidity, heat_index_c, heat_index_f, wind_condition, condition)
    return weather_string.encode('ascii')
def google_forecast(params):
    """Basically the same as google_weather but returns the forcast instead of just today"""
    url = GOOGLE_WEATHER_URL+urllib.urlencode(params)    
    response = _buildResponse(url).read()
    forecast = minidom.parseString(response).getElementsByTagName('forecast_conditions')
    #dom should be 4 elements (tommorow, +2, +3, +4) tue-fri if todays' monday
    output = ""
    for day in forecast:
        if output:
            output += " {C11}| "

        day.__getitem__=lambda s : str(day.getElementsByTagName(s)[0].getAttribute('data'))

        output += "{C3}"+day["day_of_week"]
        output += " {C2}"+day["low"]
        output += " {C5}"+day["high"]
        output += " {C10}"+day["condition"]
    return "<{C3}Forcast {C11}| "+output+" {}>"
def on_PRIVMSG(bot, sender, args): 
    PREFIX = '!'
    nick, channel, args = sender.split('!', 1)[0], args[0], args[1]
    
    if args.startswith(PREFIX):
        try:
            cmd, msg = args.split(' ', 1)
            if cmd in ["!gs", "!gsearch"]:
                query = {'q': msg}
                bot.say(channel, google_search(query))
            if cmd in ["!gw", "!gweather", "!weather"]:
                query = {'weather': msg, 'hl': 'en'}
                bot.say(channel, google_weather(query))
            if cmd in ["!gf", "!forecast"]:
                bot.say(channel, google_forecast({'weather':msg}))
            if cmd in ["!gc", "!gcalc"]:
                query = {'q': msg}
                bot.say(channel, google_calc(query))
            if cmd in ["!gd", "!gdefine"]:
                query = {'q': 'define:'+msg}
                msgparts = msg.split()
                num = 0
                try:
                    if int(msgparts[-1]):
                        num = int(msgparts.pop())
                    query = {'q': 'define:'+' '.join(msgparts)}
                except:
                    pass
                bot.say(channel, google_define(query, num=num))
            if cmd in ["!gp", "!gspell"]:
                query = {'q': msg}
                bot.say(channel, google_spell(query))
        except ValueError:
            cmd, msg = "", ""
            

