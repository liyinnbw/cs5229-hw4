#!/usr/bin/python
"""
Topology of Organization with 3 switches:
- S1 connected to h1
- S2 connected to h2
- S3 connected to h3, h4, and h5

Controller is configured to run on Localhost with tcp port:5229

Ghozali, Oct 2020
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections, custom, waitListening, decode
from mininet.log import setLogLevel, info
from mininet.node import OVSController
from mininet.cli import CLI
from mininet.node import Controller, OVSSwitch, RemoteController
import subprocess
from time import sleep
import os


myBandwidth = 100
myDelay = '10ms'
myQueueSize = 1000
myLossPercentage = 0


class BellTopo( Topo ):
    "Switches connected to n hosts."
    def build( self, n=5 ):
        pass

def multiControllerNet():
    topo = BellTopo( n=5 )

    net = Mininet( topo=topo, host=CPULimitedHost, 
        link=TCLink, controller=Controller, switch=OVSSwitch)

    print "*** Creating controllers. Make sure you run the controller at port 5229!!"
    ctrl = RemoteController( 'ctrl', ip='127.0.0.1',port=5229)
    
    print "*** Creating switches"
    s1 = net.addSwitch( 'S1' )
    s2 = net.addSwitch( 'S2' )
    s3 = net.addSwitch( 'S3' )
    print "*** Creating hosts"
    h1 = net.addHost('h1');
    h2 = net.addHost('h2');
    h3 = net.addHost('h3');
    h4 = net.addHost('h4');
    h5 = net.addHost('h5');

    print "*** Creating links"
    net.addLink(s1, h1)
    net.addLink(s2, h2)
    net.addLink(s3, h3)
    net.addLink(s3, h4)
    net.addLink(s3, h5)

    net.addLink(s1,s2, bw=myBandwidth, delay=myDelay, 
        loss=myLossPercentage, max_queue_size=myQueueSize, use_htb=True)
    net.addLink(s1,s3, bw=myBandwidth, delay=myDelay, 
        loss=myLossPercentage, max_queue_size=myQueueSize, use_htb=True)
    net.addLink(s2,s3, bw=myBandwidth, delay=myDelay, 
        loss=myLossPercentage, max_queue_size=myQueueSize, use_htb=True)

    print "*** Starting network"
    net.build()
    s1.start( [ ctrl ] )
    s2.start( [ ctrl ] )
    s3.start( [ ctrl ] )

    print "*** Running CLI"
    CLI( net )

    print "*** Stopping network"
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )  # for CLI output
    # Setup Queues in the switches
    multiControllerNet()