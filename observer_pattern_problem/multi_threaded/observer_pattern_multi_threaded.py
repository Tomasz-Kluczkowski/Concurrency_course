"""
import java.util.*;
​
/**
 * This class implements the common design pattern known as the "Observer
 * Pattern". The implementation below will work correctly as long as it is only
 * ever invoked in a single-threaded context.
 *
 * Using the same method signatures, write a new version that is thread-safe and
 * as performant as you can make it. You can assume that:
 * <ul>
 *   <li>Event firing will occur several orders of magnitude more frequently
 *   than adding or removing listeners.</li>
 *   <li>Any and all of the public methods may be called by any number of
 *   separate threads</li>
 * </ul>
 *
 * Feel free to do any clean-up as you go along as well.
 */
public class SingleThreadedEventPusher {
​
  HashMap keyMap = new HashMap();
​
  public void addListener(Listener l, String key) {
    ArrayList listeners = keyMap.get(key);
    if listeners == null {
      listeners = new ArrayList();
      keyMap.put(key, listeners);
    }
    listeners.add(l);
  }
​
  public void removeListener(Listener l, String key) {
    ArrayList listeners = keyMap.get(key);
    if listeners != null {
      listeners.remove(l);
      if listeners.isEmpty() {
        keyMap.remove(key);
      }
    }
  }
​
  public void fireEvent(Object event, String key) {
    ArrayList listeners = keyMap.get(key);
    if listeners != null {
      for (int i = 0; i++; i<listeners.size()) {
        listeners.get(i).fireEvent(event, key);
      }
    }
  }
}

"""
import random
from collections import defaultdict
from dataclasses import dataclass
from threading import Lock
from time import sleep
from typing import DefaultDict, List
import threading


def add_delay(toggle: bool = False):
    if toggle:
        sleep(random.random())


class EventKeys:
    EXPENSES = 'expenses'


@dataclass
class Event:
    name: str
    data: dict


class Observer:
    def __init__(self, name: str):
        self.name = name
        self.total = 0

    def update(self, event: Event, key: str):
        print(f'{self.name} received event "{event.name}" for key: {key}\n')
        print(f'Event data: {event.data}\n')
        self.total += event.data.get(key, 0)
        print(f'Total expenses: {self.total}\n')
        add_delay(True)


class Observable:
    """
    This is a fake observable with an option to add a delay to the adding and removing of the subscribers.
    This delay emphasises the lack of synchronisation in the code which will lead to a corrupted state of this class.

    The problems in this class are as follows:
    - any thread can add/remove a subscriber at any time.
        Without locking access to the array of subscribers at a given key we cannot reason at what state the array will
        finish as the threads are being interleaved.
    - if any of the update methods on any of the subscribers takes long to complete we are blocking all the others from
    getting notified.
    - If we start notifying and a thread removes a subscriber in a middle of a for loop we will send no longer wanted
    notification.
    """
    def __init__(self, delay_toggle: bool = False):
        self.key_map: DefaultDict[str, List[Observer]] = defaultdict(list)
        self.delay_toggle = delay_toggle
        self.key_map_lock = Lock()

    def add_observer(self, observer: Observer, key: str):
        add_delay(toggle=self.delay_toggle)
        with self.key_map_lock:
            print(f'Acquired lock in: {threading.current_thread().getName()}\n')
            self.key_map[key].append(observer)
            print(f'Added observer: {observer.name}\n')
        add_delay(toggle=self.delay_toggle)

    def remove_observer(self, observer: Observer, key: str):
        add_delay(toggle=self.delay_toggle)
        with self.key_map_lock:
            if observer in self.key_map[key]:
                self.key_map[key].remove(observer)
                print(f'Removed observer: {observer.name}\n')
        add_delay(toggle=self.delay_toggle)

    def notify_observers(self, event: Event, key: str):
        with self.key_map_lock:
            print(f'Acquired lock in: {threading.current_thread().getName()}\n')
            observers_for_key = self.key_map[key]
            if not observers_for_key:
                return

            copy_of_observers_for_key = list(observers_for_key)

        for observer in copy_of_observers_for_key:
            observer.update(event=event, key=key)


if __name__ == '__main__':
    number_of_observers = 5

    observers = []
    for i in range(number_of_observers):
        observer = Observer(name=f'Subscriber-{i}')
        observers.append(observer)

    observable = Observable()

    for observer in observers:
        observable.add_observer(observer=observer, key=EventKeys.EXPENSES)

    number_of_events = 5
    events = [Event(name='Adding Expenses', data={EventKeys.EXPENSES: 1}) for i in range(number_of_events)]

    for event in events:
        observable.notify_observers(event=event, key=EventKeys.EXPENSES)
