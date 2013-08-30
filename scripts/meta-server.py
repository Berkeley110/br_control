#!/usr/bin/env python
from SimpleXMLRPCServer import SimpleXMLRPCServer
import xmlrpclib
import subprocess
from threading import Thread
from time import sleep


START_ROS_ROVER = []    # stores roscor and rover program


class myThread (Thread):
    '''
    Class in charge of running programs a separated threads to avoid
    conflicts when sharing information
    '''
    def __init__(self, cmd):
        Thread.__init__(self)
        self.cmd = cmd
        self.cmd_process = []
    def run(self):
        self.cmd_process.append(subprocess.Popen(self.cmd))
    def stop(self):
        for process in self.cmd_process:
            process.kill()

def startProcess():
    '''
    This function starts roscore and the rovers software.
    The function is called when a client connects to the meta-server
    '''
    # commands to start roscore and the rovers ROS program
    threads = []                # stores active threads
    roscore_cmd = ['roscore']
    br_cmd = ['rosrun', 'br_swarm_rover', 'br_control.py']
    roscore_thread = myThread(roscore_cmd)
    roscore_thread.start()
    threads.append(roscore_thread)
    rover_started = False    # true if rover program started
    sleep(3)
    while not rover_started:
        try:
            rover_thread = myThread(br_cmd)
            rover_thread.start()
            rover_started = True
            threads.append(rover_thread)
        except BaseException:
            print('trying to connect to rover(s)')
            pass
    return threads

def getServerAddress():
    '''
    Meta-server calls this function when when requesting
    ROS server's address
    '''


if __name__ == '__main__':
    threads = []
    try:
        threads = startProcess() 
    except BaseException:
        print('exiting ROS program')
        for thread in threads:
            thread.stop()
        from sys import exit
        exit()
