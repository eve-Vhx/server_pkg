#!/usr/bin/env python
import rospy
from msg_pkg.srv import masterConnect, masterConnectResponse
from msg_pkg.srv import UiReq, UiReqResponse
from msg_pkg.srv import UiArmReq, UiArmReqResponse
from msg_pkg.msg import droneMasterList
from msg_pkg.msg import feedbackMsg
from action_client import ServerActionClient
from arming_check import ServerArmingCheck

class ClientConnect:

    def __init__(self,name):
        print("Server connect service started!")
        self.drone_master_array = []
        #self.mission_request = []
        self.feedback_msg = feedbackMsg()
        self.pi_connect_service = rospy.Service('pi_connect_master', masterConnect, self.handle_connect_cb)
        #self.ui_mission_req_service = rospy.Service('ui_mission_req', UiReq, self.handle_ui_mission_cb)
        #self.ui_arming_req_service = rospy.Service('ui_arming_req', UiArmReq, self.handle_ui_arming_cb)
        self.drone_master_list_pub = rospy.Publisher('QROW_master_list', droneMasterList, queue_size=10)
        self.server_master_feedback_ = rospy.Publisher('server_master_feedback', feedbackMsg, queue_size=10)
        #self.check_connections()
        rospy.Subscriber("/" + drone_id + "/connection_checks", connections_drone, self.connections_cb)

    def handle_connect_cb(self, req):
        print("Server recieved a new Rpi with id: " + req.id) #publish to server_master_feedback code: 0 drone_id: 
        self.drone_master_array.append(req.id)
        ui_master_list = droneMasterList()
        ui_master_list.drone_master_list = self.drone_master_array
        self.drone_master_list_pub.publish(ui_master_list)
        return masterConnectResponse(True)


    # def handle_ui_mission_cb(self, req):
    #     self.feedback_msg.feedback = 1
    #     self.feedback_msg.drone_id = req.drone_id
    #     self.server_master_feedback_.publish(self.feedback_msg)
    #     print("UI has asked for a mission request") #publish to server_master_feedback code: 1 drone_id
    #     self.mission_request = [req.lat, req.lon, req.alt, req.cruise_alt, req.drone_id]
    #     server_action_client = ServerActionClient(self.mission_request)

    # def handle_ui_arming_cb(self, req):
    #     self.feedback_msg.feedback = 2
    #     self.feedback_msg.drone_id = req.drone_id
    #     self.server_master_feedback_.publish(self.feedback_msg)
    #     print("UI has asked for drone to be armed") #publish to server_master_feedback code: 2 drone_id
    #     server_arming_check = ServerArmingCheck(req.drone_id, req.request_arming, rospy.Time.now().secs)
    #     print("Sent the arming request through from master")





if __name__ == '__main__':
    rospy.init_node('server_master_node', anonymous=True)
    ClientConnect(rospy.get_name())
    rospy.spin()



