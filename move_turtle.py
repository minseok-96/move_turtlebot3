#!/usr/bin/env python

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal,MoveBaseActionResult
from math import radians,degrees
from actionlib_msgs.msg import *
from geometry_msgs.msg import Point


class turtle:

    def __init__(self):

        self.goal_check=0
        self.goal_position_number=0

    def turtle_callback(self,msg):
        
        self.goal_check= msg.status.status
        if self.goal_check==3:
            self.goal_position_number+=1
        

    def move_goal(self,num):
        
        goal_position=[[-0.10,-2.05],[1.95,-0.02],[0.065,2.0],[-2.0, 0.0]]

        goal_orient=[[0.7,0.7],[1.0,0.0],[-0.7,0.7],[0.0,1.0]]

        ac = actionlib.SimpleActionClient("move_base", MoveBaseAction)

        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()

        goal.target_pose.pose.position = Point(goal_position[num][0],goal_position[num][1],0.0)

        goal.target_pose.pose.orientation.x = 0.0
        goal.target_pose.pose.orientation.y = 0.0
        goal.target_pose.pose.orientation.z = goal_orient[num][0]
        goal.target_pose.pose.orientation.w = goal_orient[num][1]

        ac.send_goal(goal)

if __name__ == "__main__":
    
    rospy.init_node("map_navigation",anonymous=False)

    my_turtle= turtle()

    turtle_sub = rospy.Subscriber("/move_base/result",MoveBaseActionResult,my_turtle.turtle_callback,queue_size=10)

    rate_=rospy.Rate(1)
    goal_position_num=0

    while not rospy.is_shutdown():
        
        my_turtle.move_goal(goal_position_num)

        rate_.sleep(5)

        goal_position_num = my_turtle.goal_position_number

        if goal_position_num > 4:
            
            break




