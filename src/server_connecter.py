#!/usr/bin/env python
import rospy
from msg_pkg.srv import masterConnect, masterConnectResponse
from msg_pkg.msg import uiMasterList
from msg_pkg.srv import UiReq


class ServerConnecter:
    def __init__(self,name):
        self.drone_ui_array = []
        self.nest_ui_array = []
        self.drone_pi_connect_service = rospy.Service('drone_pi_connect_master', masterConnect, self.handle_drone_connect_cb)
        self.nest_pi_connect_service = rospy.Service('nest_pi_connect_master', masterConnect, self.handle_nest_connect_cb)
        #self.ui_mission_service = rospy.Service('ui_mission_req', UiReq, self.handle_mission_cb)
        self.ui_drone_pub = rospy.Publisher('drone_master_list', uiMasterList, queue_size=10)
        self.ui_nest_pub = rospy.Publisher('nest_master_list', uiMasterList, queue_size=10)
        print("Started server connect service")
    
    def handle_drone_connect_cb(self,req):

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

        drone_master_msg = uiMasterList()
        drone_master_msg.ui_master_list = self.drone_ui_array
        self.ui_drone_pub.publish(drone_master_msg)

        return masterConnectResponse(True)

    def handle_nest_connect_cb(self,req):
        nest_exists = False
        for nestid in self.nest_ui_array:
            if(nestid == req.id):
                nest_exists = True

        if(not nest_exists):
            self.nest_ui_array.append(req.id)
            rospy.wait_for_service('nest_telem_connect')
            try:
                nest_telem_client = rospy.ServiceProxy('nest_telem_connect', masterConnect)
            except rospy.ServiceException as e:
                print("Cannot setup new nest for telemetry")

        nest_master_msg = uiMasterList()
        nest_master_msg.ui_master_list = self.nest_ui_array
        self.ui_nest_pub.publish(nest_master_msg)

        return masterConnectResponse(True)




if __name__ == '__main__':
    rospy.init_node('server_connecter', anonymous=True)
    ServerConnecter(rospy.get_name())
    rospy.spin()



