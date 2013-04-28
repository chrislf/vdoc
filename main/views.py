# Create your views here.
from django.http import HttpResponseServerError, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from api.views import search_with_keys, fetch_docs, unquote_qd, insert_doc

def main(request):
    return render_to_response('main.html')

def get_one(request):
    latest_doc = fetch_docs(unquote_qd(request.GET), latest=True)
    context = { 'doc': latest_doc }
    return render_to_response('get.html', context)

def view(request):
    all_matches = fetch_docs(unquote_qd(request.GET))
    context = { 'doc_list': all_matches, 'doc': all_matches[0] }
    return render_to_response('get.html', context)


@csrf_exempt
def add(request):
    if request.method == 'GET':
        return render_to_response('add.html')
    if request.method == 'POST':
        res = insert_doc(unquote_qd(request.POST))
        if res['added']:
            return HttpResponseRedirect('/')
        else:
            return render_to_response('add.html', { 'error': 'no document uploaded'})
    else:
        return HttpResponseBadRequest('%s not supported' % request.method)

def list(request):
    result = search_with_keys(['name', 'descr'])
    if not result['ok']:
        return HttpResponseServerError('search failed')
    context = { 'doc_list': [ x['_id'] for x in result['result']] }
    return render_to_response('list.html', context)
