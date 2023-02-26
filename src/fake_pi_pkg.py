#!/usr/bin/env python
import rospy
from msg_pkg.srv import masterConnect


def run_fake_client():
    rospy.wait_for_service('pi_connect_master')
    try:
        fake_pi_connect = rospy.ServiceProxy('pi_connect_master', masterConnect)
        verification = fake_pi_connect('QROW11021')
        print("Successfully connected to server")
        print(verification)
    except rospy.ServiceException as e:
        print("fake pi connect service call failed")


if __name__ == '__main__':
    rospy.init_node('fake_pi_pkg')
    run_fake_client()