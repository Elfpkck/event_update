import json
import datetime
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from event_update.models import Event


def validateKey(dict, *keys):
    '''Checks if all keys in dict.'''
    a = b = 0
    for key in keys:
        a += 1
        if key in dict:
            b += 1
    if a == b and a != 0:
        return True


def valiDateTime(date_text):
    '''Checks format of the string with datetime.'''
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%dT%H:%M:%S%z')
    except ValueError:
        return False
    else:
        return True


def validateId(eventId):
    if isinstance(eventId, int) and eventId > 0:
        return True


def counter(list, item, i):
    list.append(item)
    return i + 1


def checkData(item, i, err_list):
    '''Checks if such keys as "eventId" and 'startTime' are presented
    in dictionary and validates values.

    '''
    if validateKey(item, "eventId", 'startTime'):
        e_id = item["eventId"]
        start = item['startTime']
        if validateId(e_id) and valiDateTime(start):
            b = Event(start_time=start, external_id=e_id)
            b.save()
        else:
            i = counter(err_list, item, i)
    else:
        i = counter(err_list, item, i)
    return i


def saveData(request):
    '''Loads data from POST request and cheks if "data" in dictionary.'''
    json_data = json.loads(request.body.decode('utf-8'))
    err_list = []
    i = 0
    if validateKey(json_data, "data"):
        for item in json_data["data"]:
            i = checkData(item, i, err_list)
    return i, err_list


@csrf_exempt
def eventUpdate(request):
    '''Checks type of request. If it "POST", parses data into
    database and shows error quontity and error places.

    '''
    if request.method == 'POST':
        i, err_list = saveData(request)
        return StreamingHttpResponse('OK, errors: {} in {}'.format(i,
        err_list))
    else:
        return StreamingHttpResponse("it wasn't POST request")