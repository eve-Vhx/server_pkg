#!/usr/bin/env python
import rospy
import actionlib
from msg_pkg.msg import server_px4_reqGoal, server_px4_reqAction, server_px4_reqResult, server_px4_reqFeedback
from msg_pkg.msg import feedbackMsg
from msg_pkg.msg import armingMsg
from msg_pkg.msg import connections_drone

class ServerMissionClient:

    def __init__(self,name)
        self.connections_status = {
            "px4": False,
            "mavros": False,
            "wifi": False,
            "lte": False,
            "ros_timestamp": 0
        }
        self.ui_mission_req_service = rospy.Service('ui_mission_req', UiReq, self.handle_ui_mission_cb)

    def handle_ui_mission_cb(self, req):
        self.current_drone_id = req.drone_id
        self.action_client = actionlib.SimpleActionClient(self.current_drone_id + '/mavros/smr_px4_command/d1_cmd_action', server_px4_reqAction)
        rospy.Subscriber(req.drone_id + "/connection_checks", connections_drone, self.connections_cb)
        if(self.initialConnectPi()):
            self.sendGoal()
        else:
            print("Server action client failed to find action server")

    def connections_cb(self,data):
        self.connections_status = {
            "px4": data.px4,
            "mavros": data.mavros,
            "wifi": data.wifi,
            "lte": data.lte,
            "ros_timestamp": data.ros_timestamp.secs
        }
        print(self.connections_status)


    def initialConnectPi(self):
        return self.action_client.wait_for_server(timeout = rospy.Duration(3.0))

    def sendGoal(self):
        if(self.run_connection_checks()):

        



if __name__ == '__main__':
    rospy.init_node('server_mission_client', anonymous=True)
    ServerMissionClient(rospy.get_name())
    rospy.spin()