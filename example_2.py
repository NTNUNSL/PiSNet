import sys

from utility import ConfigUtility
from emu import SdnEmu
from net import RpiNet
from node import RpiSwitch, RpiHost, RpiController
from app import Application

print "Hello PiSNet!"

machines = ConfigUtility()
machines.read('machines.cfg')

rpinet = RpiNet()

s1 = rpinet.addSwitch( 's1', machines.get('RPI_C06') )
s2 = rpinet.addSwitch( 's2', machines.get('RPI_C07') )
s3 = rpinet.addSwitch( 's3', machines.get('RPI_C08') )
s4 = rpinet.addSwitch( 's4', machines.get('RPI_C10') )
h1 = rpinet.addHost( 'h1', machines.get('RPI_C02') )
h2 = rpinet.addHost( 'h2', machines.get('RPI_C03') )
h3 = rpinet.addHost( 'h3', machines.get('RPI_C01') )
h4 = rpinet.addHost( 'h4', machines.get('RPI_C05') )
c1 = rpinet.addController( 'c1', machines.get('RPI_C04') )

rpinet.addLink(h1, s1)
rpinet.addLink(h3, s1)
rpinet.addLink(s1, s2)
rpinet.addLink(s2, s3)
rpinet.addLink(s3, s4)
rpinet.addLink(h2, s4)
rpinet.addLink(h4, s4)

cmd = ConfigUtility()
cmd.read( sys.argv[1] )

c1.addService( cmd.get('REMOTE','NOHUP'), cmd.get('RYU') )

video_streaming = Application( cmd.get('VIDEO_STREAMING') )
video_streaming.setServer( h1, cmd.get('REMOTE','GENERAL') )
video_streaming.setClient( h2, cmd.get('REMOTE','PSEUDO_TERMINAL') )

monitoring = Application( cmd.get('MONITORING') )
monitoring.setServer( h1, cmd.get('REMOTE','GENERAL') )
monitoring.setClient( h2, cmd.get('REMOTE','GENERAL') )
monitoring.setLogNo( sys.argv[2] )

bg_traffic = Application( cmd.get('BG_TRAFFIC') )
bg_traffic.setServer( h3, cmd.get('REMOTE','GENERAL') )
bg_traffic.setClient( h4, cmd.get('REMOTE','GENERAL') )

emu = SdnEmu(rpinet)
emu.addStartQueue( monitoring )     #FIFO
emu.addStartQueue( video_streaming )
emu.addStartQueue( bg_traffic )
emu.start()

emu.callChecker( video_streaming )
emu.addStopQueue( monitoring )      #FIFO
emu.addStopQueue( bg_traffic )
emu.stop()

