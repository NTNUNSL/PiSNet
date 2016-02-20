import subprocess
import socket
import sys
from node import RpiSwitch, RpiHost, RpiController
from utility import CommandUtility

class RpiNet:

    def __init__(self):
        self._switches = []
        self._hosts = []
        self._controllers = []
        self._switch_dpid_set = []

    def get_controllers(self):
        return self._controllers

    def get_hosts(self):
        return self._hosts

    def get_switches(self):
        return self._switches

    def addSwitch(self, name, machine):
        handler = CommandUtility()
        access_ip = handler.get_access_ip(machine)
        access_port = handler.get_access_port(machine)
        dpid = handler.get_switch_dpid(access_ip, access_port)
        rpi_switch = RpiSwitch(name, machine, dpid)
        print "[add switch %s (dpid: %s)]" % ( rpi_switch.get_name(), rpi_switch.get_dpid() )
        self._switches.append(rpi_switch)
        return rpi_switch

    def addHost(self, name, machine):
        rpi_host = RpiHost(name, machine)
        print "[add host %s]" % rpi_host.get_name()
        self._hosts.append(rpi_host)
        return rpi_host
    
    def addController(self, name, machine):
        rpi_controller = RpiController(name, machine)
        print "[add controller %s]" % rpi_controller.get_name()
        self._controllers.append(rpi_controller)
        return rpi_controller

    def addLink(self, from_node, to_node):
        # Build bi-direction connection
        from_node.set_link(to_node)
        to_node.set_link(from_node)

        

