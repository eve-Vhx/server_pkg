#!/usr/bin/env python
import rospy
from msg_pkg.msg import server_px4_reqGoal, server_px4_reqAction, server_px4_reqResult, server_px4_reqFeedback

class ServerActionClient():

    def __init__(self):
        self.action_client_obj = actionlib.SimpleActionClient('/mavros/smr_px4_command/d1_cmd_action', server_px4_reqAction)