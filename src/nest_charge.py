#!/usr/bin/env python
import rospy
import actionlib
from msg_pkg.msg import NestCharge, NestChargeAction, NestChargeGoal

class NestCharge:
    def __init__(self):
        self.nest_charge_service = rospy.Service('ui_nest_charge_req', nestCharge, self.handle_charge_cb)

    def handle_charge_cb(self,req):
        self.charge_action_client = actionlib.SimpleActionClient(req.id + 'Charge_ctrl', NestChargeAction)
        self.charge_goal = NestChargeGoal(charge_drone=req.charge)
        self.charge_action_client.send_goal(self.charge_goal)

        return nestChargeResponse(True)

if __name__ == '__main__':
    rospy.init_node('nest_charge_node')
    NestCharge()
    rospy.spin()