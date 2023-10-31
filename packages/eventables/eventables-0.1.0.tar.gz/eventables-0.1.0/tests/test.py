import unittest

from src.eventables.events import Event, EventList
from tests.models import EventTestClass


class EventTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setup(self):
        pass

    def tearDown(self):
        pass

    def test_event_add(self):
        test_class = EventTestClass()
        test_class.event1 += test_class.increase_test_num
        self.assertEqual(len(test_class.event1._event_listeners), 1, "Event not successfully added")

    def test_event_remove(self):
        test_class = EventTestClass()
        test_class.event1 += test_class.increase_test_num
        test_class.event1 -= test_class.increase_test_num
        self.assertEqual(len(test_class.event1._event_listeners), 0, "Event not successfully removed")

    def test_event_run(self):
        test_class = EventTestClass()
        test_class.event1 += test_class.increase_test_num
        test_class.call_events(5)
        self.assertEqual(test_class.test_number, 5, f"Test number did not increase during event call")

    def test_event_sub_events(self):
        test_event = Event(_root=True)
        self.assertEqual(type(test_event.on_event_added), Event, "Event sub event on_event_added not created")
        self.assertEqual(type(test_event.on_event_removed), Event, "Event sub event on_event_removed not created")
        self.assertEqual(getattr(test_event.on_event_added, "on_event_added", None), None,
                         "Event sub sub event on_event_added is not None")
        self.assertEqual(getattr(test_event.on_event_added, "on_event_removed", None), None,
                         "Event sub sub event on_event_removed is not None")

    def test_event_list(self):
        event_list = EventList([1,2,3])
        test_class = EventTestClass()
        event_list.on_entry_added += test_class.increase_test_num
        event_list.on_entry_changed += test_class.increase_test_num
        event_list.on_entry_removed += test_class.increase_with_index

        event_list.append(4)
        self.assertEqual(test_class.test_number, 4, "event_list on_entry_added did not run")

        test_class.test_number = 0
        event_list.remove(4)
        self.assertEqual(test_class.test_number, 4, "event_list on_entry_removed did not run")

        test_class.test_number = 0
        event_list[2] = 4
        self.assertEqual(test_class.test_number, 4, "event_list on_entry_changed did not run")
