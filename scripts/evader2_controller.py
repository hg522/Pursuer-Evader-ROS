#!/usr/bin/env python
#license removed for brevity

import rospy
import tf
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry


velocity_publisher = rospy.Publisher('/robot_0/cmd_vel', Twist, queue_size=5)
vel = Twist ()
vel.linear.x = 2
vel.linear.y = 0
vel.linear.z = 0
vel.angular.x = 0
vel.angular.y = 0
vel.angular.z = 0

def mean(data) :
	return float(sum(data)) / max(len(data),1)

def avoidObstacle (data) :
	global vel
	global velocity_publisher
	wd = 0.8
	sd = 0.8
	av = 10
	rmin = min(data.ranges[60:90])
	lmin = min(data.ranges[91:121])
	st = data.ranges[90]	
	rf = data.ranges[0]
	lf = data.ranges[180]
	strgtleft = data.ranges[270]
	offset = 0.8
	
	if st < wd and lf < sd and rf < sd:
		vel.linear.x = 0
		vel.angular.z = av
		velocity_publisher.publish(vel)
	elif st > wd and lf < sd and rf < sd:
		if rmin < offset or lmin < offset:
			vel.linear.x = 0
			vel.angular.z = av
			velocity_publisher.publish(vel)
		else :
			vel.linear.x = 2
			vel.angular.z = 0
			velocity_publisher.publish(vel)
	elif st < wd or lmin < sd or rmin < sd or rf < sd or lf < sd:
		vel.linear.x = 0
		vel.angular.z = av
		velocity_publisher.publish(vel)
	else:
		vel.linear.x = 2
		vel.angular.z = 0
		velocity_publisher.publish(vel)

def pubtransform (data) :
	tfbr = tf.TransformBroadcaster()
	position = (data.pose.pose.position.x,
		    data.pose.pose.position.y,
		    data.pose.pose.position.z)
	orientation = (data.pose.pose.orientation.x,
		       data.pose.pose.orientation.y,
		       data.pose.pose.orientation.z,
		       data.pose.pose.orientation.w)
	time_stamp = data.header.stamp
	child_id = 'robot_0'
	header_id = 'world'
	tfbr.sendTransform(position,orientation,rospy.Time.now(),child_id,header_id)

def evader() :
	global vel
	global velocity_publisher
	rospy.init_node('evader', anonymous=True)
	laserscan_listener = rospy.Subscriber('/robot_0/base_scan', LaserScan, avoidObstacle)
	odom_listener = rospy.Subscriber('/robot_0/base_pose_ground_truth', Odometry, pubtransform)
	rospy.spin()
	

if __name__ == '__main__':
	try:
	    evader()
	except rospy.ROSInterruptException:
	    pass
		
		
	


