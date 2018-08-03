import os
import sqlite3

class pythonmq:
    def __init__(self, queuename: str, force=False):
        self.queuename = queuename
        self.force = force
        self.debug = False
    
    def enabledebug(self, param=True):
        self.debug = param

    def createnewqueue(self):
        queuename = self.queuename
        force  = self.force
        try:
            if os.path.isfile(os.environ['TMPDIR']+queuename) is True and force is False:
                raise Exception("Queue already exists. please use the command pythonmq(queuename, force=True) in order to force this queue to be created.")
            elif os.path.isfile(os.environ['TMPDIR']+queuename) is True and force is True:
                os.remove(os.environ['TMPDIR']+queuename)
            self.conn = sqlite3.connect(os.environ['TMPDIR']+queuename, isolation_level=None)
            self.c = self.conn.cursor()
            self.c.execute("""
            CREATE TABLE messages (message TEXT)
            """)
        except Exception as e:
            if self.debug is True:
                print(str(e))
            else:
                raise Exception("Failed to Create table.")
        finally:
            self.conn.commit()

    def joinqueue(self):
        queuename = self.queuename
        try:
            if os.path.isfile(os.environ['TMPDIR']+queuename) is True:
                self.conn = sqlite3.connect(os.environ['TMPDIR']+queuename, isolation_level=None)
                self.c = self.conn.cursor()
            else:
                raise Exception("Queue does not exist.")
        except Exception as e:
            if self.debug is True:
                print(str(e))
            else:
                raise Exception("Unable to connect to queue.")

    def broadcastmessage(self, *message):
        try:
            sql = "INSERT INTO messages(message) VALUES"
            for i in range(len(message)):
                if message[i] not in ("", None):
                    sql = sql+"('{}')".format(message[i])
                if i+1 != len(message):
                    sql = sql+","
            self.c.execute(sql)
        except Exception as e:
            if self.debug is True:
                print(str(e))
            else:
                raise Exception("Failed to parse message to broadcaster.")
        finally:
            self.conn.commit()
    
    def displaymessages(self, id=None):
        try:
            self.c = self.conn.cursor()
            if id is None:
                self.c.execute("""
                SELECT rowid as id,message FROM messages ORDER BY rowid ASC
                """)
            else:
                if type(id) is int:
                    self.c.execute("""
                    SELECT rowid as id,message FROM messages WHERE rowid=? ORDER BY rowid ASC
                    """, (id,))
                elif type(id) is tuple:
                    id = "SELECT rowid as id,message FROM messages WHERE rowid IN {} ORDER BY rowid ASC".format(id)
                    self.c.execute(id)
            return self.c.fetchall()
        except Exception as e:
            if self.debug is True:
                print(str(e))
            else:
                raise Exception("Failed to fetch messages.")

    def popmessage(self, last=True):
        try:
            if last is True:
                self.c = self.conn.cursor()
                self.c.execute("SELECT count(*) from messages")
                numberofrows = int(self.c.fetchone()[0])
                self.c.execute("DELETE FROM messages WHERE rowid = {}".format(numberofrows))
            else:
                self.c.execute("DELETE FROM messages WHERE rowid = {}".format(1))
        except Exception as e:
            if self.debug is True:
                print(str(e))
            else:
                raise Exception("unable to pop message from the queue.")
        finally:
            self.c.execute("VACUUM")

    def removemessagebyid(self, messageid):
        try:
            self.c = self.conn.cursor()
            if type(messageid) is int:
                self.c.execute("DELETE FROM messages WHERE rowid = {}".format(messageid))
            elif type(messageid) is tuple:
                self.c.execute("DELETE FROM messages WHERE rowid in {}".format(messageid))
            else:
                raise Exception("messageid argument must be of int type.")
        except Exception as e:
            if self.debug is True:
                print(str(e))
            else:
                raise Exception("Could not remove specified message from queue.")
        finally:
            self.c.execute("VACUUM")
    
    def closequeue(self):
        try:
            self.conn.close()
            os.remove(os.environ['TMPDIR']+self.queuename)
        except Exception as e:
            if self.debug is True:
                print(str(e))
            else:
                raise Exception("Could not close queue.")
