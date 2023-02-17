#!/usr/bin/env python
import rospy
import actionlib
from msg_pkg.msg import server_px4_reqGoal, server_px4_reqAction, server_px4_reqResult, server_px4_reqFeedback

class ServerActionClient():

    def __init__(self):
        self.action_client_obj = actionlib.SimpleActionClient('/mavros/smr_px4_command/d1_cmd_action', server_px4_reqAction)
        print("Successfully started the action client")
        self.initialConnectPi()
    
    def initialConnectPi(self):
        self.action_client_obj.wait_for_server(timeout = rospy.Duration(20.0))
        print("connected to the server")
