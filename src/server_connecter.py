#!/usr/bin/env python
import rospy
from msg_pkg.srv import masterConnect, masterConnectResponse
from msg_pkg.msg import droneMasterList
from drone_connection import DroneConnection 


class ServerConnecter:
    def __init__(self,name):
        self.drone_ui_array = []
        self.drone_obj_array = []
        self.pi_connect_service = rospy.Service('pi_connect_master', masterConnect, self.handle_connect_cb)
        self.ui_drone_pub = rospy.Publisher('drone_master_list', droneMasterList, queue_size=10)
        print("Started server connect service")
        #self.update_drone_array()
    
    def handle_connect_cb(self,req):

        exists = False
        for droneid in self.drone_ui_array:
            if(droneid == req.id):
                exists = True
        
        if(not exists):
            self.drone_ui_array.append(req.id)
            drone_obj = DroneConnection(req.id)
            self.drone_obj_array.append(drone_obj)
        print(self.drone_ui_array)
        return masterConnectResponse(True)
    
    def update_drone_array(self):
        while(not rospy.is_shutdown()):
            for droneObj in self.drone_obj_array:
                if (droneObj.updated == False):
                    for droneId in self.drone_ui_array:
                        if (droneId == droneObj.id):
                            self.drone_ui_array.remove(droneId)
                else:
                    exists_ = False
                    for droneId_ in self.drone_ui_array:
                        if(droneId_ == droneObj.id):
                            exists_ = True
                    
                    if(not exists_):
                        self.drone_ui_array.append(droneObj.id)

            drone_master_list_msg = droneMasterList()
            drone_master_list_msg.drone_master_list = self.drone_ui_array
            self.ui_drone_pub.publish(drone_master_list_msg)
            rospy.sleep(2)



if __name__ == '__main__':
    rospy.init_node('server_connecter', anonymous=True)
    ServerConnecter(rospy.get_name())
    rospy.spin()



