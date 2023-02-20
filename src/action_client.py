#!/usr/bin/env python
import rospy
import actionlib
from msg_pkg.msg import server_px4_reqGoal, server_px4_reqAction, server_px4_reqResult, server_px4_reqFeedback
from msg_pkg.msg import feedbackMsg
from msg_pkg.msg import armingMsg

class ServerActionClient():

    def __init__(self,mission_request):
        self.mission_request = mission_request
        self.arming_check_status = False
        self.arming_check_timestamp = 0
        self.action_client_obj = actionlib.SimpleActionClient(mission_request[4] + '/mavros/smr_px4_command/d1_cmd_action', server_px4_reqAction)
        self.mission_feedback_pub = rospy.Publisher(mission_request[4] + 'mission_feedback', feedbackMsg, queue_size=10)
        rospy.Subscriber(drone_id + "arming_state", armingMsg, self.arming_checks_cb)
        self.mission_feedback = feedbackMsg()
        print("Successfully started the action client") #publish to mission_feedback code: 0 drone_id:
        if(self.initialConnectPi()):
            print("Server action client has found and connected to the action server on the Pi") #publish to mission_feedback code: 1 drone_id:
            self.sendGoal()
        else:
            print("Server action client did not find the action server on the Pi") #publish to mission_feedback code: 2 drone_id
            self.mission_feedback.feedback = 2
            self.mission_feedback_pub.publish(self.mission_feedback)
    
    def initialConnectPi(self):
        return self.action_client_obj.wait_for_server(timeout = rospy.Duration(5.0))

    def sendGoal(self):
        if (self.run_arming_check):
            self.mission_goal = server_px4_reqGoal(lat=self.mission_request[0], lon=self.mission_request[1], alt=self.mission_request[2], cruise_alt=self.mission_request[3], yaw_rad=0, mission_type=0, timestamp=rospy.Time.now().secs)
            self.action_client_obj.send_goal(self.mission_goal)
            self.mission_feedback.feedback = 0
            self.mission_feedback_pub.publish(self.mission_feedback)
            print("Server action client successfully sent the goal to the pi") #publish to mission_feedback code: 3 drone_id
            self.action_client_obj.wait_for_result()
            print("Result for the action server")
            print(self.action_client_obj.get_result())
        else:
            print("Server action client failed arming check")

    def arming_checks_cb(self, msg):
        self.arming_check_status = msg.armed
        self.arming_check_timestamp = msg.timestamp

    def run_arming_check(self):
        if (self.arming_check_status == True):
            if (abs(rospy.Time.now() - self.arming_check_timestamp) < 2):
                print("Server action client successfully passed all arming checks") #publish to mission_feedback code: 6 drone_id:
                return True
            else:
                print("Server action client failed arming check because connection checks are out of date") #publish to mission_feedback code: 5 drone_id
                return False
        else:
            print("Server action client failed arming check because drone is not armed") #publish to mission_feedback code: 4 drone_id
            return False

        
