''' REST API access to the versioned document store '''

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseServerError
from django.core.exceptions import ObjectDoesNotExist
from django.utils.http import urlunquote
from vc.settings import monghost, mdb, collection
import json
from pymongo import Connection

db = Connection(monghost)[mdb][collection]

def numberify(doc):
    ''' Takes a dict and tries to
        replace its values with numbers.
    '''
    retdict = {}
    for key, value in doc.items():
        try:
            i = int(value)
            retdict[key] = i
        except ValueError:
            try:
                f = float(value)
                retdict[key] = f
            except ValueError:
                retdict[key] = value
    return retdict

def unquote_GET(GET):
    ''' return a GET as a dict
        with the keys unquoted
    '''
    d = GET.dict()
    for k in d.keys():
        d[k] = urlunquote(d[k])
    return d


def fetch_docs(qrydict, latest=False):
    ''' helper function for get_docs/get_doc.
        Also used in main/views.py
    '''
    matches = db.find(qrydict)
    if matches.count() == 0:
        raise DoesNotExist()
    if latest:
        doc = matches.sort('_id', -1).limit(1).next()
        doc.pop('_id')
        return doc
    else:
        doc_list = []
        for doc in matches:
            doc.pop('_id')
            doc_list.append(doc)
        return doc_list


def get_docs(request):
    ''' Returns all versions of a document.
        If multiple documents match, all
        versions of matching documents are returned.
    '''
    if request.method != 'GET':
        return HttpResponseBadRequest('% not supported' % request.method)
    try:
        doc_list = fetch_docs(unquote_GET(request.GET))
    except DoesNotExist:
        return HttpResponseNotFound()

    try:
        jdoc = json.dumps(doc_list)
    except ValueError:
        return HttpResponseServerError('Document list not JSON-formattable')
    return HttpResponse(jdoc, mimetype='application/json')


def get_doc(request):
    ''' Returns the most recent version of a document.
        If multiple documents match, the most recent of
        all the matched documents is returned.
    '''
    if request.method != 'GET':
        return HttpResponseBadRequest('% not supported' % request.method)

    try:
        latest_doc = fetch_docs(unquote_GET(request.GET.dict()), latest=True)
    except DoesNotExist:
        return HttpResponseNotFound()

    try:
        jdoc = json.dumps(latest_doc)
    except ValueError:
        return HttpResponseServerError('Document not JSON-formattable')
    return HttpResponse(jdoc, mimetype='application/json')


def add_doc(request):
    ''' Attempts to add the POSTed document to the
        datastore. If successful returns the current
        number of versions in the db.
    '''
    if request.method != 'POST':
        return HttpResponseBadRequest('% not supported' % request.method)
    doc = request.POST.dict()
    cleaned_doc = numberify(doc)
    db.update(cleaned_doc, cleaned_doc, upsert=True)
    total = db.find(cleaned_doc).count()
    res = {'result': 'success', 'total_docs': total}
    return HttpRepsonse(json.dumps(res), mimetype='application.json')


def search_with_keys(keylist):
    ''' helper function for list_docs.
        Also used in main/views.py
    '''
    mdict = dict([ (x, { '$exists': True }) for x in keylist ]) # for the mongo agg query
    gdict = dict([ (x, '$' + x) for x in keylist ]) # for the mongo agg group
    results = db.aggregate(
            [
                { '$match': mdict },
                { '$group':
                    { '_id': gdict }
                }
            ]
    )
    return results


def list_docs(request):
    ''' Returns a list of documents for which
        the keys in the request correspond
        to valid fields.
    '''
    if request is None:
        keys = keylist
    else:
        if request.method != 'GET':
            return HttpResponseBadRequest('% not supported' % request.method)
        keys = request.GET.dict().keys()
    if len(keys) == 0:
        return HttpResponseBadRequest('need at least one field to search for')
    results = search_with_keys(keys)
    if not results['ok']:
        return HttpResponseServerError('query failed')
    docs = [ x['_id'] for x in results['result'] ]
    try:
        jdocs = json.dumps(docs)
    except ValueError:
        return HttpResponseServerError('could not format results as JSON')
    return HttpResponse(jdocs, mimetype='application/json')
