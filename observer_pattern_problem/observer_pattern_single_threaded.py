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
from collections import defaultdict
from dataclasses import dataclass
from typing import DefaultDict, Set


class EventKeys:
    EXPENSES = 'expenses'


@dataclass
class Event:
    name: str
    data: dict


class Subscriber:
    def __init__(self, name: str):
        self.name = name
        self.total = 0

    def update(self, event: Event, key: str):
        print(f'{self.name} received event "{event.name}" for key: {key}')
        print(f'Event data: {event.data}')
        self.total += event.data.get(key, 0)
        print(f'Total expenses: {self.total}')


class Observable:
    def __init__(self):
        self.key_map: DefaultDict[str, Set[Subscriber]] = defaultdict(set)

    def add_subscriber(self, subscriber: Subscriber, key: str):
        self.key_map[key].add(subscriber)

    def remove_subscriber(self, subscriber: Subscriber, key: str):
        self.key_map[key].discard(subscriber)

    def notify_subscribers(self, event: Event, key: str):
        for subscriber in self.key_map[key]:
            subscriber.update(event=event, key=key)


number_of_subscribers = 5

subscribers = []
for i in range(number_of_subscribers):
    subscriber = Subscriber(name=f'Subscriber-{i}')
    subscribers.append(subscriber)


observable = Observable()

for subscriber in subscribers:
    observable.add_subscriber(subscriber=subscriber, key=EventKeys.EXPENSES)

number_of_events = 5
events = [Event(name='Adding Expenses', data={EventKeys.EXPENSES: 1}) for i in range(number_of_events)]

for event in events:
    observable.notify_subscribers(event=event, key=EventKeys.EXPENSES)
