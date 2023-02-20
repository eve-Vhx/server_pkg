#!/usr/bin/env python
import rospy
from msg_pkg.msg import feedbackMsg
from msg_pkg.msg import connections_drone
from msg_pkg.msg import armingMsg

class ArmingCheck:

    __init__(self, drone_id, request_arming):
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
        if (self.connections_status["px4"] == False or self.connections_status["mavros"] == False):
            return False
        elif (abs(rospy.Time.now().secs - self.connections_status["ros_timestamp"]) > 2):
            return False
        else:
            return True


    def run_arming_check(self):
        while(!rospy.is_shutdown()):
            if (self.run_connection_checks()):
                if (self.request_arming == True):
                    self.arming_state.armed = True
                    self.arming_state.timestamp = rospy.Time.now().secs
                    self.arming_pub.publish(self.arming_state)
                else:
                    self.arming_state.armed = False
                    self.arming_state.timestamp = rospy.Time.now().secs
                    self.arming_pub.publish(self.arming_state)
            else:
                self.arming_state.armed = False
                self.arming_state.timestamp = rospy.Time.now().secs
                self.arming_pub.publish(self.arming_state)



    

