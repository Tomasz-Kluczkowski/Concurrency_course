from threading import Thread

from observer_pattern_problem.multi_threaded.observer_pattern_multi_threaded import Observer, Event, Observable


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
    def test_add_observers_in_multiple_threads(self):
        repeats = 10
        for _ in range(repeats):
            number_of_threads = 10000
            observable = Observable(delay_toggle=True)
            observers = [Observer(name=f'test_name-{i}') for i in range(number_of_threads)]
            key = 'test_key'

            threads = []
            for i in range(number_of_threads):
                thread = Thread(target=observable.add_observer, kwargs={'observer': observers[i], 'key': key})
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()
            sorted_observers = sorted(observers, key=lambda observer: id(observer))
            expected_observers = sorted(observable.key_map[key], key=lambda observer: id(observer))
            assert sorted_observers == expected_observers

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
        number_of_observers = 10
        number_of_events = 10

        observers = []
        for i in range(number_of_observers):
            observer = Observer(name=f'test_name-{i}')
            observers.append(observer)

            observable.add_observer(observer=observer, key=key)

        events = [Event(name=f'Test Event-{i}', data={key: 1}) for i in range(number_of_events)]

        for event in events:
            observable.notify_observers(event=event, key=key)

        for observer in observers:
            assert observer.total == len(events)

    def test_notifies_observers_mixed_with_register(self):
        observable = Observable(delay_toggle=True)
        key = 'test_key'
        number_of_observers = 10

        observers = []
        for i in range(number_of_observers):
            observer = Observer(name=f'test_name-{i}')
            observers.append(observer)

            observable.add_observer(observer=observer, key=key)

        number_of_events = 10
        event_value = 5
        events = [Event(name=f'Test Event-{i}', data={key: event_value}) for i in range(number_of_events)]

        notify_threads = []
        for event in events:
            notify_thread = Thread(
                target=observable.notify_observers, kwargs={'event': event, 'key': key}, name=f'Notify Thread for event: {event.name}'
            )
            notify_threads.append(notify_thread)
            notify_thread.start()

        additional_observer = Observer(name='Added During Notify')
        add_observer_thread = Thread(
            target=observable.add_observer,
            kwargs={'observer': additional_observer, 'key': key},
            name='Add Observer Thread',
        )
        add_observer_thread.start()

        for notify_thread in notify_threads:
            notify_thread.join()
        add_observer_thread.join()

        assert len(observable.key_map[key]) == number_of_observers + 1
        for observer in [observer for observer in observers if observer is not additional_observer]:
            assert observer.total == event_value * number_of_events
