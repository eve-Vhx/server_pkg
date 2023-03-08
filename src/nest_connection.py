#!/usr/bin/env python
import rospy
from msg_pkg.srv import masterConnect, masterConnectResponse
from msg_pkg.msg import NestBeaconActionFeedback, NestChargeActionFeedback
from msg_pkg.msg import nestTelemMsg, fakeChargeMsg, fakeBeaconMsg
from msg_pkg.srv import NestGPSMessage

import threading


class NestConnection:
    def __init__(self, id):
        self.timer = threading.Timer(5,self.timeout)
        self.nest_connect_service = rospy.Service(id + 'nest_telem_connect', masterConnect, self.run_routine)

    def run_routine(self,req):
        print("Nest connection node called with id: " + req.id)
        self.id = req.id
        rospy.Subscriber(self.id + '/Charge_cntl/feedback', NestChargeActionFeedback, self.charging_cb)
        rospy.Subscriber(self.id + '/Beacon_cntl/feedback', NestBeaconActionFeedback, self.beacon_cb)
        self.charging = False
        self.beacon_on = False
        self.connected = False
        self.gps = [0,0,0]
        self.nest_telem_pub = rospy.Publisher(self.id + '/ui_nest_telem', nestTelemMsg, queue_size=10)
        self.publish_nest_data()

        self.timer.start()

        return masterConnectResponse(True)

    def timeout(self):
        rospy.wait_for_service(self.id + '/nest_gps')
        try:
            gps_client = rospy.ServiceProxy(self.id + '/nest_gps', NestGPSMessage)
            gps_res = gps_client()
            self.gps = [gps_res.latitude, gps_res.longitude, gps_res.altitude]
        except rospy.ServiceException as e:
            print("GPS Service call failed: %s"%e)

    def charging_cb(self,msg):
        self.charging = msg.feedback.charging
       
    def beacon_cb(self,msg):
        self.beacon_on = msg.feedback.beacon_on

    def publish_nest_data(self):
        while (not rospy.is_shutdown()):
            nest_telem_msg = nestTelemMsg()
            nest_telem_msg.charging = self.charging
            nest_telem_msg.beacon = self.beacon_on
            nest_telem_msg.connected = self.connected
            nest_telem_msg.lat = self.gps[0]
            nest_telem_msg.lon = self.gps[1]
            nest_telem_msg.alt = self.gps[2]
            self.nest_telem_pub.publish(nest_telem_msg)
            print(self.gps)
            rospy.sleep(1)
