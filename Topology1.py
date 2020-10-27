#!/usr/bin/python
"""
Topology of Organization with 2 switches(S1 and S2) S1 is connected to h1 and h2 while S2 is connected to h3 and h4 

Controller is configured to run on Localhost with tcp port:5229

Ghozali, Aug 2020
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import OVSController
from mininet.cli import CLI
from mininet.node import Controller, OVSSwitch, RemoteController
import subprocess
import os


myBandwidth = 10
myDelay = '100ms'
myQueueSize = 1000
myLossPercentage = 0


class BellTopo( Topo ):
    "Switches connected to n hosts."
    def build( self, n=4 ):
        pass

def multiControllerNet():
    topo = BellTopo( n=4 )

    net = Mininet( topo=topo, host=CPULimitedHost, 
        link=TCLink, controller=Controller, switch=OVSSwitch)

    print "*** Creating controllers. Make sure you run the controller at port 5229!!"
    ctrl = RemoteController( 'ctrl', ip='127.0.0.1',port=5229)
    
    print "*** Creating switches"
    s1 = net.addSwitch( 'S1' )
    s2 = net.addSwitch( 'S2' )
    print "*** Creating hosts"
    h1 = net.addHost('h1', mac='00:00:00:00:00:01');
    h2 = net.addHost('h2', mac='00:00:00:00:00:02');
    h3 = net.addHost('h3', mac='00:00:00:00:00:03');
    h4 = net.addHost('h4', mac='00:00:00:00:00:04');

    print "*** Creating links"
    net.addLink(s1, h1)
    net.addLink(s1, h2)
    net.addLink(s2, h3)
    net.addLink(s2, h4)

    net.addLink(s1,s2, bw=myBandwidth, delay=myDelay, 
        loss=myLossPercentage, max_queue_size=myQueueSize, use_htb=True)

    print "*** Starting network"
    net.build()
    s1.start( [ ctrl ] )
    s2.start( [ ctrl ] )

    print "*** Running CLI"
    CLI( net )

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )  # for CLI output
    # Setup Queues in the switches
    multiControllerNet()