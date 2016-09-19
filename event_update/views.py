import json
from datetime import datetime
from django.http import StreamingHttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from event_update.models import Event
from time import gmtime, strftime
from django.views.generic import View


class EventUpdate(View):
    def validateKey(self, dict, *keys):
        '''Checks if all keys in dict.'''
        a = b = 0
        for key in keys:
            a += 1
            if key in dict:
                b += 1
        if a == b and a != 0:
            return True

    def validate5Min(self, date_text):
        """Compares present UTC +0 time with time from input string.
        If time from input string bigger than 300 seconds, return true.

        """
        now = strftime('%Y-%m-%dT%H:%M:%S%z', gmtime())
        now = datetime.strptime(now, '%Y-%m-%dT%H:%M:%S%z')
        date_text = datetime.strptime(date_text, '%Y-%m-%dT%H:%M:%S%z')
        diff = date_text - now
        if diff.days > 0 or (diff.days == 0 and diff.seconds > 300):
            return True

    def valiDateTime(self, date_text):
        '''Checks format of the string with datetime.'''
        try:
            datetime.strptime(date_text, '%Y-%m-%dT%H:%M:%S%z')
        except ValueError:
            return False
        else:
            return self.validate5Min(date_text)

    def validateId(self, eventId):
        if isinstance(eventId, int) and eventId > 0:
            return True

    def counter(self, list, item, i):
        list.append(item)
        return i + 1

    def checkData(self, item, i, err_list):
        '''Checks if such keys as "eventId" and 'startTime' are presented
        in dictionary and validates values.

        '''
        if self.validateKey(item, "eventId", 'startTime'):
            e_id = item["eventId"]
            start = item['startTime']
            if self.validateId(e_id) and self.valiDateTime(start):
                b = Event(start_time=start, external_id=e_id)
                b.save()
            else:
                i = self.counter(err_list, item, i)
        else:
            i = self.counter(err_list, item, i)
        return i

    def saveData(self, request):
        '''Loads data from POST request and cheks if "data" in dictionary.'''
        json_data = json.loads(request.body.decode('utf-8'))
        err_list = []
        i = 0
        if self.validateKey(json_data, "data"):
            for item in json_data["data"]:
                i = self.checkData(item, i, err_list)
        return i, err_list

    @method_decorator(csrf_exempt)
    def eventUpdate(self, request):
        '''Checks type of request. If it is "POST", parses data into
        database and shows error quontity and error places.

        '''
        if request.method == 'POST':
            i, err_list = self.saveData(request)
            return StreamingHttpResponse('OK, errors: {} in {}'.format(i,
            err_list))
        else:
            return StreamingHttpResponse("it wasn't POST request")