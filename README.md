# PythonMQ
Pure python implementation of a basic MQ (based on sqlite3) for local machine use (ideal for basic IPC).


## How does it work?
- It creates a sqlite3 file at the UNIX/Linux TEMP directory with the name of the queue. A queue is created and all messages are stored inside the sqlite3 file.
- All queue messages are stored in the sqlite3 file and indexed by row number.
- It brings the "pop" concept of stack allocation (it pops the last message), you also can remove the first message or a specific one.
- has a debug feature to print exceptions (no need to edit lib files).

## Libs needed
- sqlite3
- os

Basically native libs of python 3

## Class Methods
- **__init__(queuename, force=False)** constructor method. Used to parse queue's name to the class and set variables. The argument force is used when a queue db file with the same name already exists. In this type of case, just parse the arg "force=True" when instancing the class
- **enabledebug(param=True)** Used to change debuging (in case you call this method, it will print any and all exceptions to the terminal). In case you wish to disable debug just parse de arg **param=False**.
- **createnewqueue()** Used to create and join a new queue with the name you parsed to the constructor method when invoking the class.
- **joinqueue()** Joins the queue you parsed to the constructor method when invoking the class (the queue must already exist).
- **broadcastmessage(message)** Send the message you wish to the database (queue you created), so all clients can access it. you can parse a single message, or multiple messages. Ex.: broadcastmessage("message1") or broadcastmessage("message2, "message3")
- **displaymessages(id=None)** Method used to display messages of the queue. In case no argumenta are parsed, this method will return all messages available to this queue. In case you need a specific message just parse the id arg with the number of the message "displaymessages(id=1)", in case you need a group of messages, just parse a tuple with the ids "displaymessages(id=(1,3)). This method will return a List containing tuples with the answers. Ex.: [(1, "message1",), (2, "message2",)].
- **popmessage(last=True)** Pops (removes) the last message of the queue. In case you need to remove/pop the first message, just parse the arg last as false "last=False".
- **removemessagebyid(messageid)** Removes a message by its specific id. you can parse the id (as interger) or a tuple of ids (tuple of intergers) as arguments. Ex.: removemessagebyid(1) or removemessagebyid((5,6,7))
- **closequeue()** Closes the queue and deletes the file from the temp directory

## Basic Usage
```python
from pythonmq import *
q = pythonmq("myownqueue", force=True)
q.createnewqueue()
q.broadcastmessage("message1")
q.broadcastmessage("message2", "message3", "message4")
q.displaymessages()
```
output:
```shell
[(1, 'message1'), (2, 'message2'), (3, 'message3'), (4, 'message4')]
```
```python
q.popmessage()
q.displaymessages()
```
output:
```shell
[(1, 'message1'), (2, 'message2'), (3, 'message3')]
```
```python
q.removemessagebyid(2)
q.displaymessages()
q.closequeue()
```
output:
```shell
[(1, 'message1'),(2, 'message3')]
```
- Note that the order of the messages are rearranges. Now the message3 is now the 2nd message