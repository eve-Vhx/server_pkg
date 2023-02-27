#!/usr/bin/env python
import rospy
from msg_pkg.srv import masterConnect, masterConnectResponse
from msg_pkg.msg import NestBeaconFeedback, NestChargeFeedback
from msg_pkg.msg import nestTelemMsg

class NestConnection:
    def __init__(self):
        self.nest_connect_service = rospy.Service('nest_telem_connect', masterConnect, self.run_routine)

    def run_routine(self,req):
        self.id = req.id
        rospy.Subscriber(self.id + '/Charge_cntl/feedback', NestChargeFeedback, self.charging_cb)
        rospy.Subscriber(self.id + '/Beacon_cntl/feedback', NestBeaconFeedback, self.beacon_cb)
        self.charging = False
        self.beacon_on = False
        self.connected = False
        self.nest_telem_pub = rospy.Publisher(self.id + 'ui_nest_telem', nestTelemMsg)
