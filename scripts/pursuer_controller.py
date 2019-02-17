#!/usr/bin/env python
#license removed for brevity

import roslib
import rospy
import tf
import math
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from tf2_msgs.msg import TFMessage

pursuerPose = Odometry()

def pubtransform (data) :
	global pursuerPose
	pursuerPose = data
	tfbr = tf.TransformBroadcaster()
	position = (data.pose.pose.position.x,
		    data.pose.pose.position.y,
		    data.pose.pose.position.z)
	orientation = (data.pose.pose.orientation.x,
		       data.pose.pose.orientation.y,
		       data.pose.pose.orientation.z,
		       data.pose.pose.orientation.w)
	time_stamp = data.header.stamp
	child_id = 'robot_1'
	header_id = 'world'
	tfbr.sendTransform(position,orientation,rospy.Time.now(),child_id,header_id)


def pursuer() :
	rospy.init_node('pursuer', anonymous=True)
	velocity_publisher = rospy.Publisher('/robot_1/cmd_vel', Twist, queue_size=5)
	odom_listener = rospy.Subscriber('/robot_1/base_pose_ground_truth', Odometry, pubtransform)
	vel = Twist ()
		
	rate = rospy.Rate(10) #10 Hz
	tf_listener = tf.TransformListener()
	while not rospy.is_shutdown() :
		if rospy.Time.now().to_sec() > rospy.Duration(1.0).to_sec() :
			try:
				now = rospy.Time.now()			
				past = now - rospy.Duration(1.0)					
				tf_listener.waitForTransformFull('/robot_1',now,'/robot_0',past,'/world', rospy.Duration(1.0))
				(translation,orientation) = tf_listener.lookupTransformFull('/robot_1',now,'/robot_0',past,'/world')			
			except :
				continue
			
			h = math.sqrt(translation[0] ** 2 + translation[1] ** 2) 
			'''
			we calculate the translation that should come around to 2 since the velocity of evader is 2 
			and we are taking a delay of 1 sec i.e h = vel * time , so our pursuer should also move at 
			a speed of around 2. But we multiply later with a factor of 0.6 so that when evader stops, the pursuer doesnt crash into it.
			'''
			
			theta = math.atan2(translation[1], translation[0])
			''' calculating angle in radians'''
			
			av = 15 * h * theta
			'''we calculate the angular velocity by using r*theta and here multiply with a factor of 15
			to make the robot turn faster'''

			vel.linear.x = 0.6 * h
			vel.angular.z = av
			velocity_publisher.publish(vel) 			
		   	
	rospy.spin()

# reference taken from tf tutorials link provided in project pdf

if __name__ == '__main__':
	try:
	    pursuer()
	except rospy.ROSInterruptException:
	    pass
		

