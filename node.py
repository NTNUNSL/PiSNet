import time
import copy
import subprocess
from utility import CommandUtility
from app import Program

class RpiNode(object):

    def __init__(self, name, machine):
        self._name = name
        self._machine = machine
        self._links = []

    def set_link(self, to_node):
        self._links.append(to_node)

    def get_name(self):
        return self._name

    def get_machine(self):
        return self._machine

    def get_all_links(self):
        return self._links


class RpiSwitch(RpiNode):
    
    def __init__(self, name, machine, dpid):
        super(RpiSwitch, self).__init__(name, machine)
        self._dpid = dpid

    def get_dpid(self):
        return self._dpid

    def clear_table(self):
        handler = CommandUtility()
        access_ip = handler.get_access_ip(self._machine)
        access_port = handler.get_access_port(self._machine)
        cmd = handler.get_clear_table_cmd(access_ip, access_port)
        subprocess.call(cmd, shell=True)
        print "Clear the flow table of the switch " + self._name + " (dpid: " + self._dpid + ")"


class RpiHost(RpiNode):

    def __init__(self, name='', machine={}):
        super(RpiHost, self).__init__(name, machine)
        self._program = Program()

    def get_program(self):
        return self._program

    def set_program_name(self, program_name):
        self._program.set_name(program_name)

    def set_program_cmd(self, cmd):
        self._program.set_cmd(cmd)
    
    def clone(self, rpi_host):
        self._name = rpi_host.get_name()
        self._machine = copy.deepcopy( rpi_host.get_machine() )

    def start(self):
        subprocess.call(self._program.get_cmd(), shell=True)
        print "The program [" + self._program.get_name()  + "] on " + self._name + " is start ..."
        time.sleep(5)
        handler = CommandUtility()
        access_ip = handler.get_access_ip(self._machine)
        access_port = handler.get_access_port(self._machine)
        search_process_cmd = handler.get_search_process_cmd( access_ip, access_port, self._program.get_name() )
        pid = subprocess.check_output(search_process_cmd, shell=True)
        self._program.set_pid(pid)
        print "The PID on " + self._name + " is " + self._program.get_pid()

    def stop(self):
        handler = CommandUtility()
        access_ip = handler.get_access_ip(self._machine)
        access_port = handler.get_access_port(self._machine)
        kill_process_cmd = handler.get_kill_process_cmd( access_ip, access_port, self._program.get_pid() )
        subprocess.call(kill_process_cmd, shell=True)
        print "kill the PID on " + self._name + ": " + self._program.get_pid()
        print "The program [" + self._program.get_name()  + "] on " + self._name + " is stop ..."


class RpiController(RpiHost):

    def __init__(self, name, machine):
        super(RpiController, self).__init__(name, machine)

    def addService(self, remote_cmd, controller):
        handler = CommandUtility()
        self._program.set_name( handler.get_program_name(controller) )
        machine_content = self._machine.values().pop()
        remode_cmd = handler.replace(remote_cmd, machine_content)
        exec_cmd = remode_cmd + " " + handler.get_controller_service(controller)
        self._program.set_cmd(exec_cmd)


