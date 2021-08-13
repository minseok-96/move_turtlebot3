#!/usr/bin/env python
# -*- coding: utf-8 -*-


import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal,MoveBaseActionResult
from math import radians,degrees
from actionlib_msgs.msg import *
from geometry_msgs.msg import Point

# 추가할 사항

#장소 마커 표시하기
#기다리기 & map clear 기능

#--> 배달로봇 만들기


class turtle:

    def __init__(self):

        self.goal_check=0
        self.goal_position_number=0
        self.wait=True
        self.wait_time=0

    def turtle_callback(self,msg):
        
        self.goal_check= msg.status.status
        # print("goal={}".format(self.goal_check ))
        print("goal_time={}".format(self.wait_time))
        if self.goal_check==3:

            self.wait_time+=1

            if self.wait_time==5:
                self.wait=False

            if self.wait==False:
                self.goal_position_number+=1
                self.wait=True
        else:
            self.wait_time=0

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

        rate_.sleep()

        goal_position_num = my_turtle.goal_position_number

        if goal_position_num > 3:
            
            break





