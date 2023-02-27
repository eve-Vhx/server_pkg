#!/usr/bin/env python
import rospy
from msg_pkg.srv import masterConnect, masterConnectResponse
from msg_pkg.msg import droneMasterList
from msg_pkg.srv import UiReq


class ServerConnecter:
    def __init__(self,name):
        self.drone_ui_array = []
        self.drone_obj_array = []
        self.drone_mission_array = []
        self.pi_connect_service = rospy.Service('pi_connect_master', masterConnect, self.handle_connect_cb)
        self.ui_mission_service = rospy.Service('ui_mission_req', UiReq, self.handle_mission_cb)
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
            rospy.wait_for_service('drone_telem_connect')
            try:
                telem_client = rospy.ServiceProxy('drone_telem_connect', masterConnect)
            except rospy.ServiceException as e:
                print("Cannot setup new drone for telemetry")
        print(self.drone_ui_array)
        return masterConnectResponse(True)

    def handle_mission_cb(self,req):
        print("UI has asked to send a mission through to drone")



if __name__ == '__main__':
    rospy.init_node('server_connecter', anonymous=True)
    ServerConnecter(rospy.get_name())
    rospy.spin()



