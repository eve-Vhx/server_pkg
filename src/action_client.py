#!/usr/bin/env python
import rospy
import actionlib
from msg_pkg.msg import server_px4_reqGoal, server_px4_reqAction, server_px4_reqResult, server_px4_reqFeedback

class ServerActionClient():

    def __init__(self,mission_request):
        print(mission_request[4] + '/mavros/smr_px4_command/d1_cmd_action')
        self.action_client_obj = actionlib.SimpleActionClient(mission_request[4] + '/mavros/smr_px4_command/d1_cmd_action', server_px4_reqAction)
        print("Successfully started the action client")
        if(self.initialConnectPi()):
            print("Ready to send a goal to the action server")
            self.sendInitialGoal()
        else:
            print("Could not connect to the action server for " + mission_request[4])
    
    def initialConnectPi(self):
        return self.action_client_obj.wait_for_server(timeout = rospy.Duration(5.0))

    def sendInitialGoal(self):
        self.init_goal = server_px4_reqGoal(lat=0, lon=0, alt=0, yaw_rad=0, cruise_alt=0, mission_type=9)
        self.action_client_obj.send_goal(self.init_goal)
        self.action_client_obj.wait_for_result()
        print("Result for the action server")
        print(self.action_client_obj.get_result())

        
