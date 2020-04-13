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
from typing import DefaultDict, List


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
        print(f'{self.name} received event "{event.name}" for key: {key}')
        print(f'Event data: {event.data}')
        self.total += event.data.get(key, 0)
        print(f'Total expenses: {self.total}')


class Observable:
    def __init__(self):
        self.key_map: DefaultDict[str, List[Observer]] = defaultdict(list)

    def add_observer(self, observer: Observer, key: str):
        self.key_map[key].append(observer)

    def remove_observer(self, observer: Observer, key: str):
        if observer in self.key_map[key]:
            self.key_map[key].remove(observer)

    def notify_observers(self, event: Event, key: str):
        for observer in self.key_map[key]:
            observer.update(event=event, key=key)


if __name__ == '__main__':
    number_of_observers = 5

    observers = []
    for i in range(number_of_observers):
        observer = Observer(name=f'Observer-{i}')
        observers.append(observer)

    observable = Observable()

    for observer in observers:
        observable.add_observer(observer=observer, key=EventKeys.EXPENSES)

    number_of_events = 5
    events = [Event(name='Adding Expenses', data={EventKeys.EXPENSES: 1}) for i in range(number_of_events)]

    for event in events:
        observable.notify_observers(event=event, key=EventKeys.EXPENSES)
