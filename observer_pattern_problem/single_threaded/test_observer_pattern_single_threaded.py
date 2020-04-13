from observer_pattern_problem.single_threaded.observer_pattern_single_threaded import Observer, Event, Observable


class TestSubscriber:
    def test_update(self):
        subscriber = Observer(name='test_subscriber')

        assert subscriber.total == 0
        key = 'test_key'
        value = 1
        event = Event(name='test_event', data={key: value})
        subscriber.update(event=event, key=key)

        assert subscriber.total == value


class TestObservable:
    def test_add_observer(self):
        observable = Observable()
        observer = Observer(name='test_name')
        key = 'test_key'

        observable.add_observer(observer=observer, key=key)

        [expected_observer] = observable.key_map[key]
        assert expected_observer is observer

    def test_remove_existing_observer(self):
        observable = Observable()
        observer = Observer(name='test_name')
        key = 'test_key'

        assert not observable.key_map[key]
        observable.add_observer(observer=observer, key=key)
        assert len(observable.key_map[key]) == 1

        observable.remove_observer(observer=observer, key=key)
        assert not observable.key_map[key]

    def test_remove_non_existing_observer(self):
        observable = Observable()
        observer = Observer(name='test_name')
        key = 'test_key'

        assert not observable.key_map[key]
        observable.remove_observer(observer=observer, key=key)
        assert not observable.key_map[key]

    def test_notifies_observers(self):
        observable = Observable()
        key = 'test_key'

        observers = []
        for i in range(2):
            observer = Observer(name=f'test_name-{i}')
            observers.append(observer)

            observable.add_observer(observer=observer, key=key)

        number_of_events = 5
        event_value = 5
        events = [Event(name=f'Test Event-{i}', data={key: event_value}) for i in range(number_of_events)]

        for event in events:
            observable.notify_observers(event=event, key=key)

        for observer in observers:
            assert observer.total == number_of_events * event_value
