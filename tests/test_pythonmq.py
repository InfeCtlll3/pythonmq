import unittest
import sys
import os
sys.path.append("..")
from pythonmq import pythonmq

class TestMQ(unittest.TestCase):
    def setUp(self):
        self.mq = pythonmq("testunit", force=True)
        self.mq.createnewqueue()

    def tearDown(self):
        self.mq.closequeue()

    def test_createqueue(self):
        self.assertEqual(os.path.isfile(os.environ['TMPDIR']+'testunit'), True)

    def test_joinqueue(self):
        self.assertEqual(self.mq.joinqueue(), True)
    
    def test_broadcastmessages(self):
        self.mq.broadcastmessage("t1")
        self.assertEqual(self.mq.displaymessages(), [(1, 't1')])
        self.mq.broadcastmessage("t2", "t3", "t4")
        self.assertEqual(self.mq.displaymessages(), [(1, 't1'), (2, 't2'), (3, 't3'), (4, 't4')])
        self.assertEqual(self.mq.displaymessages(id=2), [(2, 't2')])
    
    def test_popanddelete(self):
        self.mq.broadcastmessage("t1", "t2", "t3", "t4", "t5", "t6")
        self.mq.popmessage()
        self.assertNotIn((6, "t6"), self.mq.displaymessages())
        self.mq.popmessage(last=False)
        self.assertNotIn((1, "t1"), self.mq.displaymessages())
        # CHECK IF VACUUM WORKED AND THE T2 VALUE MUST BE THE 1ST ON THE LIST
        self.assertEqual(self.mq.displaymessages(id=1), [(1, "t2")])
        # at this point, our list is t2,t3,t4,t5
        self.mq.removemessagebyid(2) #remove value of t3 (index 2) of our list
        self.assertEqual(len(self.mq.displaymessages()), 3)
        self.assertEqual(self.mq.displaymessages(id=2), [(2, "t4")])

    def test_debug(self):
        with self.assertRaises(TypeError):
            self.mq.enabledebug = "test"
        self.mq.enabledebug = True
        self.assertEqual(self.mq.enabledebug, True)

    def test_closequeue(self):
        self.mq.closequeue()
        self.assertEqual(os.path.isfile(os.environ['TMPDIR']+'testunit'), False)