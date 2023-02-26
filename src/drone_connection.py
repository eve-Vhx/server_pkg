#!/usr/bin/env python
import rospy
from msg_pkg.msg import connections_drone
from msg_pkg.msg import feedbackMsg
from msg_pkg.msg import telemMsg

from mavros_msgs.msg import GPSRAW
from mavros_msgs.msg import State
from sensor_msgs.msg import Range
from geometry_msgs.msg import TwistStamped
from sensor_msgs.msg import BatteryState


class DroneConnection:
    def __init__(self,id):
        print("Successfully created new drone object!")
        self.id = id
        rospy.Subscriber(id + "/connection_checks", connections_drone, self.connections_cb)
        self.updated = False
        self.drone_connecter_feedback = rospy.Publisher(id + "drone_connecter_feedback", feedbackMsg, queue_size=10)
        self.drone_telem_pub = rospy.Publisher(id + "ui_telem_data", telemMsg, queue_size=10)

        #MAVROS telemetry data
        self.mavros_telem_gps = {
            "lat" : 0,
            "lon" : 0,
            "alt" : 0
        }
        self.mavros_telem_state = {
            "state" : " ",
            "armed" : False
        }
        self.mavros_telem_dystancez = {
            "dist_z" : 0
        }
        self.mavros_telem_vel = {
            "vel_x" : 0,
            "vel_y" : 0,
            "vel_z" : 0
        }
        self.mavros_telem_battery = {
            "battery_percent" : 0
        }
        rospy.Subscriber(id + "/mavros/gpsstatus/gps1/raw", GPSRAW, self.mavros_gps_cb)
        rospy.Subscriber(id + "/mavros/state", State, self.mavros_state_cb)
        rospy.Subscriber(id + "/mavros/distance_sensor/hrlv_ez4_pub", Range, self.mavros_distancez_cb)
        rospy.Subscriber(id + "/mavros/setpoint_velocity/cmd_vel", TwistStamped, self.mavros_vel_cb)
        rospy.Subscriber(id + "/mavros/battery", BatteryState, self.mavros_battery_cb)

        self.publish_telem_data()
        


    def connections_cb(self,msg):
        if (msg.mavros == True and msg.px4 == True):
            self.updated = True

    def mavros_gps_cb(self,data):
        self.mavros_telem_gps = {
            "lat" : data.lat*10**(-7),
            "lon" : data.lon*10**(-7),
            "alt" : data.alt*10**(-3)
        }
    
    def mavros_state_cb(self,data):
        self.mavros_telem_state = {
            "state" : data.mode,
            "armed" : data.armed
        }

    def mavros_distancez_cb(self,data):
        self.mavros_telem_dystancez = {
            "dist_z" : data.range
        }

    def mavros_vel_cb(self,data):
        self.mavros_telem_vel = {
            "vel_x" : data.twist.linear.x,
            "vel_y" : data.twist.linear.y,
            "vel_z" : data.twist.linear.z
        }

    def mavros_battery_cb(self,data):
        self.mavros_telem_battery = {
            "battery_percent" : data.percentage
        }

    def publish_telem_data(self):
        while(not rospy.is_shutdown()):
            ui_telem_msg = telemMsg()
            ui_telem_msg.lat = self.mavros_telem_gps["lat"]
            ui_telem_msg.lon = self.mavros_telem_gps["lon"]
            ui_telem_msg.alt = self.mavros_telem_gps["alt"]
            ui_telem_msg.state = self.mavros_telem_state["state"]
            ui_telem_msg.armed = self.mavros_telem_state["armed"]
            ui_telem_msg.dist_z = self.mavros_telem_dystancez["dist_z"]
            ui_telem_msg.vel_x = self.mavros_telem_vel["vel_x"]
            ui_telem_msg.vel_y = self.mavros_telem_vel["vel_y"]
            ui_telem_msg.vel_z = self.mavros_telem_vel["vel_z"]
            ui_telem_msg.battery = self.mavros_telem_battery["battery_percent"]

            self.drone_telem_pub.publish(ui_telem_msg)
            rospy.sleep(1)
            