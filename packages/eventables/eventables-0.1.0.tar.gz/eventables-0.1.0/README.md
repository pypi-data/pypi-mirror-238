# SimpleEvents
Simple Event Handler and utility objects for monitoring and responding to changes in data structures.

## Changelog
### 0.1.0 Initial Release
* Implemented generic Event() object for event processing
* Implemented EventList(). Custom list with events to respond to adding, removal, and change of entries. 
And responding to clearing of List.
## Installation
> pip install eventables

### Event() Usage
~~~python
from eventables.events import Event

class MyObject:
    def __init__(self):
        self.my_event = Event()
    
    def trigger_example(self):
        # do stuff
        self.my_event(my_arg="Successful Event Call")
        
def reaction_function(my_arg):
    print(my_arg)

def demo():
    my_object = MyObject()
    my_object.my_event += reaction_function
    my_object.trigger_example()
~~~
### Output
~~~docstring
>>> demo()
Successful Event Call
~~~
### EventList() Usage

List
~~~python
from eventables.events import EventList

class MyObject:
    def __init__(self):
        self.my_list = EventList()
        
def reaction_function(value):
    print(f"Successfully added {value} to list!")

def demo():
    my_object = MyObject()
    my_object.my_list.on_entry_added += reaction_function
    my_object.my_list.append("Test Object")
~~~
### Output
~~~docstring
>>> demo()
Successfully added Test Object to list!
~~~