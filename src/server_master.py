#!/usr/bin/env python
import rospy
from msg_pkg.srv import masterConnect

class ClientConnect():

    def __init__(self,name):
        pi_connect_service = rospy.Service('pi_connect_master', masterConnect, self.handle_connect_cb)

    def handle_connect_cb(self, res):
        print("recieved a pi!")





if __name__ == '__main__':
    rospy.init_node('server_master_node', anonymous=True)



