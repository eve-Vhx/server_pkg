#!/usr/bin/env python
import rospy
import actionlib
from msg_pkg.msg import server_px4_reqGoal, server_px4_reqAction, server_px4_reqResult, server_px4_reqFeedback

class DroneMission:
    def __init__(self,id):
        print("successfully created new drone mission object")
        self.id = id
        self.send_mission = False
        self.mission_goal = []
        self.connected_server = False
        self.mission_action_client = actionlib.SimpleActionClient(id + '/mavros/smr_px4_command/d1_cmd_action', server_px4_reqAction)

        self.run_routine()

    def initiate_connection(self):
        return self.mission_action_client.wait_for_server(timeout=rospy.Duration(5.0))

    def send_goal_pi(self):
        self.send_mission = False
        mission_goal_msg = server_px4_reqGoal(lat=self.mission_goal[0], lon=self.mission_goal[1], alt=self.mission_goal[2], yaw_rad=0, timestamp=rospy.Time.now().secs, mission_type=2, cruise_alt=10)
        self.mission_action_client.send_goal(mission_goal_msg)
        self.mission_action_client.wait_for_result()
        print(self.mission_action_client.get_result())

    def run_routine(self):
        while(not rospy.is_shutdown()):
            if(self.send_mission == True):
                if(self.initiate_connection() == True):
                    self.connected_server = True
                    self.send_goal_pi()
                else:
                    self.connected_server = False
                    print("The action client not connected to the pi server")
            else:
                print("Not sending mission due to send mission set to false")
                
