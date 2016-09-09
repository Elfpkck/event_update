from django.test import TestCase
from event_update.models import Event
from event_update.views import *



class TestInput(TestCase):
    def testValidateKey(self):
        dict = {'a':1, 'b':2, 'c':3}
        self.assertIn('a', dict)
        self.assertIn('b', dict)
        self.assertEqual(validateKey(dict, 'a', 'b'), True)

    def testValiDateTime(self):
        self.assertEqual(valiDateTime("2016-09-02T06:17:00+0800"), True)

    def testValidateId(self):
        self.assertEqual(validateId(25), True)


class EventTestCase(TestCase):
    def setUp(self):
        start_time = "2016-09-02T06:17:00+0800"
        Event.objects.create(start_time=start_time, external_id=42)

    def testData(self):
        obj = Event.objects.get(external_id=42)
        self.assertEqual(obj.is_published, True)