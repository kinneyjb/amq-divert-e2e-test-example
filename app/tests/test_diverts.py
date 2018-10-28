# from app import EventLogger
from proton import Message


def test_diverts(
        protons,
        blocking_sender,
        blocking_receiver_for_events
):

    message = Message(body='test')
    # message.subject = 'pdr.discovered'
    message.properties = {
        'subject': 'pdr.discovered'
    }
    message.address = 'events'
    message.durable = True

    blocking_sender.send(message)

    expected_events_count = 9
    actual_events = []

    try:
        for i in range(expected_events_count):
            message = blocking_receiver_for_events.receive(timeout=1)
            actual_events.append(message)
    except:
        pass

    assert expected_events_count == len(actual_events)
