#!/usr/bin/env python
import rospy
from msg_pkg.srv import masterConnect, masterConnectResponse
from msg_pkg.msg import droneMasterList
from action_client import ServerActionClient

class ClientConnect:

    def __init__(self,name):
        self.drone_master_array = []
        self.pi_connect_service = rospy.Service('pi_connect_master', masterConnect, self.handle_connect_cb)
        self.drone_master_list_pub = rospy.Publisher('QROW_master_list', droneMasterList, queue_size=10)
        print("Server connect service started!")

    def handle_connect_cb(self, req):
        print("recieved a pi!")
        print(req.id)
        self.drone_master_array.append(req.id)
        ui_master_list = droneMasterList()
        ui_master_list.drone_master_list = self.drone_master_array
        self.drone_master_list_pub.publish(ui_master_list)
        #server_action_client = ServerActionClient(req.id)
        return masterConnectResponse(True)





if __name__ == '__main__':
    rospy.init_node('server_master_node', anonymous=True)
    ClientConnect(rospy.get_name())
    rospy.spin()



