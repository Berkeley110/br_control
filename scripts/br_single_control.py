#!/usr/bin/env python
import roslib; roslib.load_manifest('br_swarm_rover')
import rospy
from std_msgs.msg import String

import br_cam
from br_control import RovCon

# meta_server.py creates the file where the ROS shall write its
# address, then the name is passed as an argument here
import argparse
parser = argparse.ArgumentParser('br_rover_client')
parser.add_argument('file', type=str,
    default=None, help='temporary file to store server uri')
arg = parser.parse_args()

if __name__ == '__main__':
    try:
        # create file to save ROS server address
        address_file = open(arg.file, 'w+b')
        # store ROS server address
        #TODO: change the local host part to a normal address
        # for now the wanted address is exported manually in the
        # .bashrc file
        import os
        address = os.environ['ROS_MASTER_URI']
        address_file.write(address)
        address_file.close()

        rover = RovCon() 
        rover_video = br_cam.RovCam(rover.return_data())
       # rover_video.receive_image()

#        pub = rospy.Publisher('chatter', String)
        rospy.init_node('AC13_robot')
        rospy.Subscriber("move", String, rover.print_test)

        distance = 0.5    # feet
        speed = 1         # foot/sec
        str = "robot moves %s" % rospy.get_time()
        rospy.loginfo(str)
        rospy.spin()
#        while not rospy.is_shutdown(): 
#            str = "robot moves %s" % rospy.get_time()
#            rospy.loginfo(str)
#            rover_video.receive_image()
#            rover.move_forward(distance, speed)

#        rover.disconnect_rover()
#        rover_video.disconnect_video()
    except rospy.ROSInterruptException:
        rover.disconnect_rover()
        rover_video.disconnect_video()
        pass