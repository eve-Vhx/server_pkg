#!/usr/bin/env python
import rospy
import actionlib
from msg_pkg.msg import server_px4_reqGoal, server_px4_reqAction, server_px4_reqResult, server_px4_reqFeedback

class ServerActionClient():

    def __init__(self,id):
        self.action_client_obj = actionlib.SimpleActionClient(id + '/mavros/smr_px4_command/d1_cmd_action', server_px4_reqAction)
        print("Successfully started the action client")
        if(self.initialConnectPi()):
            print("Ready to send a goal to the action server")
        else:
            print("Could not connect to the action server for " + id)
    
    def initialConnectPi(self):
        return self.action_client_obj.wait_for_server(timeout = rospy.Duration(5.0))
        
