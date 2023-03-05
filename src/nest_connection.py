#!/usr/bin/env python3
import rospy
from msg_pkg.srv import masterConnect, masterConnectResponse
from msg_pkg.msg import NestBeaconFeedback, NestChargeFeedback
from msg_pkg.msg import nestTelemMsg, fakeChargeMsg, fakeBeaconMsg

class NestConnection:
    def __init__(self, id):
        self.nest_connect_service = rospy.Service(id + 'nest_telem_connect', masterConnect, self.run_routine)

    def run_routine(self,req):
        print("Nest connection node called with id: " + req.id)
        self.id = req.id
        rospy.Subscriber(self.id + '/Charge_cntl/feedback', fakeChargeMsg, self.charging_cb)
        rospy.Subscriber(self.id + '/Beacon_cntl/feedback', fakeBeaconMsg, self.beacon_cb)
        self.charging = False
        self.beacon_on = False
        self.connected = False
        self.nest_telem_pub = rospy.Publisher(self.id + 'ui_nest_telem', nestTelemMsg, queue_size=10)
        self.publish_nest_data()

        return masterConnectResponse(True)

    def charging_cb(self,msg):
        self.charging = msg.charging

    def beacon_cb(self,msg):
        self.beacon_on = msg.beacon_on

    def publish_nest_data(self):
        while (not rospy.is_shutdown()):
            nest_telem_msg = nestTelemMsg()
            nest_telem_msg.charging = self.charging
            nest_telem_msg.beacon = self.beacon_on
            nest_telem_msg.connected = self.connected

            self.nest_telem_pub.publish(nest_telem_msg)
            rospy.sleep(1)

