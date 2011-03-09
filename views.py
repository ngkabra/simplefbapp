'''A very simple facebook app using python

Change the variables below appropriately
'''

APP_ID  = '<PUT YOUR APP ID HERE>'
APP_KEY = '<PUT YOUR APP KEY HERE>'
APP_SECRET = '<PUT YOUR APP SECRET HERE>'
APP_CANVAS_PAGE = 'http://apps.facebook.com/<YOUR APP NAME>/'
APP_CALLBACK_PAGE = '<PUT YOUR APP CALLBACK PAGE HERE>'

APP_CONSUMER = (APP_KEY, APP_SECRET, APP_CALLBACK_PAGE)

import base64
import hashlib
import hmac
import simplejson as json
from urllib import quote

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings

from simpleoauth import Client, providers


### BEGIN https://gist.github.com/495149
### This code is adapted from https://gist.github.com/495149 by Sunil Arora

def base64_url_decode(inp):
    padding_factor = (4 - len(inp) % 4) % 4
    inp += "="*padding_factor 
    return base64.b64decode(unicode(inp).translate(dict(zip(map(ord, u'-_'), u'+/'))))

def parse_signed_request(signed_request, secret):

    l = signed_request.split('.', 2)
    encoded_sig = l[0]
    payload = l[1]

    sig = base64_url_decode(encoded_sig)
    data = json.loads(base64_url_decode(payload))

    if data.get('algorithm').upper() != 'HMAC-SHA256':
        return None
    else:
        expected_sig = hmac.new(secret, msg=payload, digestmod=hashlib.sha256).digest()

    if sig != expected_sig:
        return None
    else:
        return data

### END of https://gist.github.com/495149

def process_request(request):
    fbdata = parse_signed_request(request.GET.get('signed_request'),
                                   APP_SECRET)
    if 'oauth_token' in fbdata:
        fbapi = Client(APP_CONSUMER, providers.facebook,
                       access_token=fbdata['oauth_token'])

    else:
        fbapi = None

    return (fbdata, fbapi)

def canvas(request):
    signed_req = request.GET.get('signed_request')
    if not signed_req:
        return render_to_response('simplefbapp/canvas.html',
                                  data=dict(message='No signed_request. Did you forget to turn on OAuth 2.0 in the Advanced Settings for your app?',
                                            APP_CANVAS_PAGE=APP_CANVAS_PAGE),
                                  context_instance=RequestContext(request))
    
    fbdata, fbapi = process_request(request)
    if not fbapi:
        # redirect user to app auth page
        redirect_url = 'https://www.facebook.com/dialog/oauth?client_id=%s&redirect_uri=%s' % (APP_ID, quote(APP_CANVAS_PAGE))
        return render_to_response('simplefbapp/auth.html',
                                  dict(redirect_url=redirect_url),
                                  context_instance=RequestContext(request))

    me_data = fbapi.get('me')
    username = me_data['first_name'] + ' ' + me_data['last_name']
    return render_to_response('simplefbapp/canvas.html',
                              dict(username=username,
                                   APP_CANVAS_PAGE=APP_CANVAS_PAGE),
                              context_instance=RequestContext(request))
    
def news(request):
    fbdata, fbapi = process_request(request)
    news = fbapi.get('me/home')
    return render_to_response('simplefbapp/news.html',
                              dict(news=news,
                                   APP_CANVAS_PAGE=APP_CANVAS_PAGE),
                              context_instance=RequestContext(request))

def friends(request):
    fbdata, fbapi = process_request(request)
    friends = fbapi.get('me/friends')
    return render_to_response('simplefbapp/friends.html',
                              dict(friends=friends,
                                   APP_CANVAS_PAGE=APP_CANVAS_PAGE),
                              context_instance=RequestContext(request))

