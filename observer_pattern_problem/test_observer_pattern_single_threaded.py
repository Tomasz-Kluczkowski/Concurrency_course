from observer_pattern_problem.observer_pattern_single_threaded import Subscriber, Event, Observable


class TestSubscriber:
    def test_update(self):
        subscriber = Subscriber(name='test_subscriber')

        assert subscriber.total == 0
        key = 'test_key'
        value = 1
        event = Event(name='test_event', data={key: value})
        subscriber.update(event=event, key=key)

        assert subscriber.total == value


class TestObservable:
    def test_add_subscriber(self):
        observable = Observable()
        subscriber = Subscriber(name='test_name')
        key = 'test_key'

        observable.add_subscriber(subscriber=subscriber, key=key)

        [expected_subscriber] = observable.key_map[key]
        assert expected_subscriber is subscriber

    def test_remove_existing_subscriber(self):
        observable = Observable()
        subscriber = Subscriber(name='test_name')
        key = 'test_key'

        assert not observable.key_map[key]
        observable.add_subscriber(subscriber=subscriber, key=key)
        assert len(observable.key_map[key]) == 1

        observable.remove_subscriber(subscriber=subscriber, key=key)
        assert not observable.key_map[key]

    def test_remove_non_existing_subscriber(self):
        observable = Observable()
        subscriber = Subscriber(name='test_name')
        key = 'test_key'

        assert not observable.key_map[key]
        observable.remove_subscriber(subscriber=subscriber, key=key)
        assert not observable.key_map[key]

    def test_notifies_subscribers(self):
        observable = Observable()
        key = 'test_key'

        subscribers = []
        for i in range(2):
            subscriber = Subscriber(name=f'test_name-{i}')
            subscribers.append(subscriber)

            observable.add_subscriber(subscriber=subscriber, key=key)

        events = [Event(name=f'Test Event-{i}', data={key: 1}) for i in range(2)]

        for event in events:
            observable.notify_subscribers(event=event, key=key)

        for subscriber in subscribers:
            assert subscriber.total == len(events)
