import os
import sqlite3
import uuid

class pythonmq(object):
    def __init__(self, queuename: str, force=False, tmp_arg=None):
        self.queuename = queuename
        self.force = force
        self.debug = False
        self.tmp_dir = ''
        if tmp_arg is None:
            try:
                self.tmp_dir = os.environ['TMPDIR']
            except KeyError:
                self.tmp_dir = '/tmp/'
        else:
            self.tmp_dir = tmp_arg

    @property
    def enabledebug(self):
        return self.debug

    @enabledebug.setter
    def enabledebug(self, param):
        if type(param) != bool:
            raise TypeError("Type of the param parsed is not supported. You must parse either True or False")
        else:
            self.debug = param
    
    def join(self):
        queuename = self.queuename
        force = self.force
        db_exists = os.path.isfile(self.tmp_dir+queuename)
        try:
            if force is True and db_exists:
                os.remove(self.tmp_dir+queuename)
                db_exists = False
            self.conn = sqlite3.connect(self.tmp_dir+queuename, isolation_level=None)
            self.c = self.conn.cursor()
            if db_exists is False:
                self.c.execute("""
                CREATE TABLE messages (message TEXT, uuid TEXT)
                """)
        except Exception as e:
            if self.debug is True:
                print(str(e))
            else:
                raise Exception("Failed to Create queue.")
        finally:
            self.conn.commit()

    def publish(self, *message, ack=True, uid=None):
        try:
            sql = "INSERT INTO messages(message, uuid) VALUES"
            ack_flag = uid if uid is not none else str(uuid.uuid4())
            to_return = ''
            for i in range(len(message)):
                if message[i] not in ("", None):
                    sql = sql+"('{}'".format(message[i]) +  ", '{}')".format(ack_flag)
                if i+1 != len(message):
                    sql = sql+","
            self.c.execute(sql)
            if ack:
                to_return = ack_flag
        except Exception as e:
            if self.debug is True:
                print(str(e))
            else:
                raise Exception("Failed to parse message to broadcaster.")
        finally:
            self.conn.commit()
            if ack:
                return to_return
    
    def display(self, id=None, with_id=False):
        try:
            self.c = self.conn.cursor()
            result = ''
            if id is None:
                self.c.execute("""
                SELECT rowid as id,message,uuid FROM messages ORDER BY rowid ASC
                """)
                result = self.c.fetchall()
            else:
                if type(id) is int:
                    self.c.execute("""
                    SELECT rowid as id,message,uuid FROM messages WHERE uuid=? ORDER BY rowid ASC
                    """, (id,))
                elif type(id) is tuple:
                    id = "SELECT rowid as id,message,uuid FROM messages WHERE uuid IN {} ORDER BY rowid ASC".format(id)
                    self.c.execute(id)
                result = self.c.fetchall()
        except Exception as e:
            if self.debug is True:
                print(str(e))
            else:
                raise Exception("Failed to fetch messages.")
        finally:
            if with_id is True:
                return result
            else:
                return [v[1] for v in result]

    def pop(self, with_id=False):
        try:
            self.c = self.conn.cursor()
            self.c.execute("""
                    SELECT rowid as id,message,uuid FROM messages WHERE rowid={}
                    """.format(1))
            result = self.c.fetchone()
            self.c.execute("DELETE FROM messages WHERE rowid = {}".format(1))
        except Exception as e:
            if self.debug is True:
                print(str(e))
            else:
                raise Exception("unable to pop message from the queue.")
        finally:
            self.c.execute("VACUUM")
            if with_id is True:
                return result
            else:
                return result[1]

    def remove_by_token(self, token):
        try:
            self.c = self.conn.cursor()
            if type(token) is str:
                self.c.execute("DELETE FROM messages WHERE uuid = {}".format(token))
            elif type(token) is tuple:
                self.c.execute("DELETE FROM messages WHERE uuid in {}".format(token))
            else:
                raise Exception("token argument must be of str type.")
        except Exception as e:
            if self.debug is True:
                print(str(e))
            else:
                raise Exception("Could not remove specified message from queue.")
        finally:
            self.c.execute("VACUUM")
    
    def close(self):
        try:
            self.conn.close()
            if os.path.isfile(self.tmp_dir+self.queuename) is True:
                os.remove(self.tmp_dir+self.queuename)
        except Exception as e:
            if self.debug is True:
                print(str(e))
            else:
                raise Exception("Could not close queue.")
