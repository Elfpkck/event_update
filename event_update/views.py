import json
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from event_update.models import Event


def save_data(request):
    json_data = json.loads(request.body.decode('utf-8'))
    for item in json_data["data"]:
        b = Event(start_time=item["startTime"], external_id=item["eventId"])
        b.save()


@csrf_exempt
def event_update(request):
    if request.method == 'POST':
        save_data(request)
        return StreamingHttpResponse('OK')
    else:
        return StreamingHttpResponse("it wasn't POST request")