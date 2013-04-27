# Create your views here.
from django.http import HttpResponseServerError
from django.shortcuts import render_to_response
from api.views import search_with_keys, fetch_docs, unquote_GET

def main(request):
    return render_to_response('main.html')

def get(request):
    latest_doc = fetch_docs(unquote_GET(request.GET), latest=True)
    context = { 'doc': latest_doc }
    return render_to_response('get.html', context)

def add(request):
    return render_to_response('add.html')

def list(request):
    result = search_with_keys(['name', 'descr'])
    if not result['ok']:
        return HttpResponseServerError('search failed')
    context = { 'doc_list': [ x['_id'] for x in result['result']] }
    return render_to_response('list.html', context)
