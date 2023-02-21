#!/usr/bin/env python
import rospy
from msg_pkg.msg import feedbackMsg
from msg_pkg.msg import connections_drone
from msg_pkg.msg import armingMsg

class ServerArmingCheck:

    def __init__(self, drone_id, request_arming):
        self.connections_status = {
            "px4": False,
            "mavros": False,
            "wifi": False,
            "lte": False,
            "ros_timestamp": 0
        }
        self.drone_id = drone_id
        self.request_arming = request_arming
        self.arming_feedback_pub = rospy.Publisher(drone_id + 'arming_feedback', feedbackMsg, queue_size=10)
        self.arming_pub = rospy.Publisher(drone_id + 'arming_state', armingMsg, queue_size=10)
        rospy.Subscriber(drone_id + "connection_checks", connections_drone, self.connections_cb)
        self.arming_feedback = feedbackMsg()
        self.arming_state = armingMsg()
        self.run_arming_check()

    def connections_cb(self, data):
        self.connections_status = {
            "px4": data.px4,
            "mavros": data.mavros,
            "wifi": data.wifi,
            "lte": data.lte,
            "ros_timestamp": data.ros_timestamp.secs
        }

    def run_connection_checks(self):
        if (self.connections_status["mavros"] == False):
            self.arming_feedback.feedback = 2
            self.arming_feedback.drone_id = self.drone_id
            self.arming_pub.publish(self.arming_feedback)
            print("Server arming request failed because mavros is offline") #publish to arming_feedback code: 2
            return False
        elif (self.connection_checks["px4"] == False):
            self.arming_feedback.feedback = 3
            self.arming_feedback.drone_id = self.drone_id
            self.arming_pub.publish(self.arming_feedback)
            print ("Server arming request failed because px4 is offline") #publish to arming_feedback code: 3
            return False
        elif (abs(rospy.Time.now().secs - self.connections_status["ros_timestamp"]) > 2):
            self.arming_feedback.feedback = 4
            self.arming_feedback.drone_id = self.drone_id
            self.arming_pub.publish(self.arming_feedback)
            print ("Server arming request failed because the time delay is too large for connection checks") #publish to arming_feedback code: 4
            return False
        else:
            self.arming_feedback.feedback = 5
            self.arming_feedback.drone_id = self.drone_id
            self.arming_pub.publish(self.arming_feedback)
            print ("Server arming request succeeded in connection checks") #publish to arming_feedback code: 5
            return True


    def run_arming_check(self):
        while(not rospy.is_shutdown()):
            if (self.run_connection_checks()):
                if (self.request_arming == True):
                    self.arming_feedback.feedback = 0
                    self.arming_feedback.drone_id = self.drone_id
                    self.arming_pub.publish(self.arming_feedback)
                    print("Server arming request succeeded!") #publish to arming_feedback code: 0 
                    self.arming_state.armed = True
                else:
                    self.arming_feedback.feedback = 1
                    self.arming_feedback.drone_id = self.drone_id
                    self.arming_pub.publish(self.arming_feedback)
                    print("Server disarming request successfully changed arming to disarmed") #publish to arming_feedback code: 1
                    self.arming_state.armed = False
            else:
                self.arming_state.armed = False
            
            self.arming_state.timestamp = rospy.Time.now().secs
            self.arming_pub.publish(self.arming_state)

            rospy.sleep(1)



    

