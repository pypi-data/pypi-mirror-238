import io
import unittest

from seaplane.common import sse


# A very poorly, but understandable stream of events.
payload = """
event:
id
data: foo

event: different
id: 5
data: multiple
data: lines


retry: 300

:comment
:this entire event is ignored

event: different2
id: 6
data: one line

:don't pass an id, also a comment
data: bar
id

data: baz
id: 8

"""


class TestSSE(unittest.TestCase):
    def test_events(self):
        stream = io.BytesIO(payload.encode("utf-8"))
        reader = sse.Reader(stream, encoding="utf-8", retry=5000)

        first_message = next(reader)
        self.assertEqual(first_message.event, "message")
        self.assertEqual(first_message.data, "foo")
        self.assertEqual(first_message.id, None)
        self.assertEqual(reader.retry, 5000)

        second_message = next(reader)
        self.assertEqual(second_message.event, "different")
        self.assertEqual(second_message.data, "multiple\nlines")
        self.assertEqual(second_message.id, "5")
        self.assertEqual(reader.retry, 5000)

        third_message = next(reader)
        self.assertEqual(third_message.event, "message")
        self.assertEqual(third_message.data, None)
        self.assertEqual(third_message.id, None)
        self.assertEqual(reader.retry, 300)

        # Comment message completely discarded

        fourth_message = next(reader)
        self.assertEqual(fourth_message.event, "different2")
        self.assertEqual(fourth_message.data, "one line")
        self.assertEqual(fourth_message.id, "6")
        self.assertEqual(reader.retry, 300)

        fifth_message = next(reader)
        self.assertEqual(fifth_message.event, "message")
        self.assertEqual(fifth_message.data, "bar")
        self.assertEqual(fifth_message.id, None)
        self.assertEqual(reader.last_event_id, "6")
        self.assertEqual(reader.retry, 300)

        sixth_message = next(reader)
        self.assertEqual(sixth_message.event, "message")
        self.assertEqual(sixth_message.data, "baz")
        self.assertEqual(sixth_message.id, "8")
        self.assertEqual(reader.last_event_id, "8")
        self.assertEqual(reader.retry, 300)

        with self.assertRaises(StopIteration):
            next(reader)
