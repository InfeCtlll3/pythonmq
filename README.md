# PythonMQ
Pure python implementation of a basic MQ (based on sqlite3) for local machine use (ideal for basic IPC).

## Limitations
- It only runs on UNIX Like machines (Linux, BSD, MacOS X).
- It's only capable of queue/distribute messages locally (cannot distribute and queue messages over the network) because the queueDB is stored locally.

## Installing
- The installing package of this lib can be found in the release section of the PythonMQ github or just clone and install the package using the following method:
```shell
git clone https://github.com/InfeCtlll3/pythonmq.git
cd pythonmq
python3 setup.py sdist
cd dist
pip3 install pythonmq-1.0.0.tar.gz
```

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
- **__init__(queuename, force=False, tmp_arg=None)** constructor method. Used to parse queue's name to the class and set variables. The argument force is used when you need to be sure that the message queue will be empty when you create it (cleanup if there is any old database with same name). The argument tmp_arg is used to specify the folder where the database will be created. In case it's not parsed, it will try to fetch the TMPDIR variable from your system or just simply use /tmp/.
- **enabledebug = Param** Function used to change debuging mode (in case you call this method, it will print any and all exceptions to the terminal). In case you wish to disable debug just set the variable **enabledebug = False**. Keep in mind that this function is set to be a property function, so it behaves like a variable.
- **join()** Joins the queue you parsed to the constructor method when invoking the class. In case the queue does not exist it will create it. You can parse **force=True** in the constructor method so force a new queue to always be created (cleanup).
- **publish(message)** Send the message you wish to the database (queue you created), so all clients can access it. you can parse a single message, or multiple messages. Ex.: publish("message1") or publish("message2, "message3")
- **display(id=None, with_id=False)** Method used to display messages of the queue. In case no arguments are parsed, this method will return all messages available to this queue. In case you need a specific message just parse the id arg with the number of the message "display(id=1)", in case you need a group of messages, just parse a tuple with the ids "display(id=(1,3)). This method will return a List of messages. Ex.: ['message1', 'message2', 'message3']. In case where you also require the message id (message order in the queue) alongside the message content, you can parse the argument "with_id=True" and you will receive a List of tuples such as: [(1, 'message1'), (2, 'message2'), (3, 'message3')].
- **pop(with_id=False)** Pops first message of the queue. This will return the first message. If you wish to return the index of the message alongside the message, use the argument "with_id=True" and you will receive a tuple as response. E.g.: (1, 'message1').
- **remove_by_id(messageid)** Removes a message by its specific id. you can parse the id (as interger) or a tuple of ids (tuple of intergers) as arguments. Ex.: removemessagebyid(1) or removemessagebyid((5,6,7))
- **close()** Closes the queue and deletes the file from the temp directory

## Basic Usage
```python
from pythonmq import *
queue = pythonmq("myownqueue", force=True)
queue.enabledebug = True
queue.join()
queue.publish("message1")
queue.publish("message2", "message3", "message4")
queue.display(with_id=True)
```
output:
```shell
[(1, 'message1'), (2, 'message2'), (3, 'message3'), (4, 'message4')]
```
```python
queue.pop()
queue.display()
```
output:
```shell
['message2', 'message3', 'message4']
```
```python
queue.remove_by_id(2)
queue.display()
```
output:
```shell
['message2', 'message4']
```
- Note that the order of the messages are rearranged. Now the message4 is the 2nd message in the queue at the moment.

If you wish to join in another process in the same queue, you just need to not use **force=True**.

- in a different python process
```python
from pythonmq import *
queue = pythonmq("myownqueue")
queue.join()
queue.display(with_id=True)
```
output:
```shell
[(1, 'message2'),(2, 'message4')]
```