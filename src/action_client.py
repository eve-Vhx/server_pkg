#!/usr/bin/env python
import rospy
import actionlib
from msg_pkg.msg import server_px4_reqGoal, server_px4_reqAction, server_px4_reqResult, server_px4_reqFeedback
from msg_pkg.msg import feedbackMsg

class ServerActionClient():

    def __init__(self,mission_request):
        self.mission_request = mission_request
        self.action_client_obj = actionlib.SimpleActionClient(mission_request[4] + '/mavros/smr_px4_command/d1_cmd_action', server_px4_reqAction)
        self.mission_feedback_pub = rospy.Publisher(mission_request[4] + 'mission_feedback', feedbackMsg, queue_size=10)
        self.mission_feedback = feedbackMsg()
        print("Successfully started the action client")
        if(self.initialConnectPi()):
            print("Ready to send a goal to the action server")
            self.sendGoal()
        else:
            print("Could not connect to the action server for " + mission_request[4])
            self.mission_feedback = 1
            self.mission_feedback_pub.publish(self.mission_feedback)
    
    def initialConnectPi(self):
        return self.action_client_obj.wait_for_server(timeout = rospy.Duration(5.0))

    def sendGoal(self):
        self.mission_goal = server_px4_reqGoal(lat=self.mission_request[0], lon=self.mission_request[1], alt=self.mission_request[2], cruise_alt=self.mission_request[3], yaw_rad=0, mission_type=0, timestamp=rospy.Time.now().secs)
        self.action_client_obj.send_goal(self.mission_goal)
        self.mission_feedback.feedback = 0
        self.mission_feedback_pub.publish(self.mission_feedback)
        self.action_client_obj.wait_for_result()
        print("Result for the action server")
        print(self.action_client_obj.get_result())

        
