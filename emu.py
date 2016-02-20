import subprocess
import threading
import time
from utility import CommandUtility

is_running = False
lock = threading.Lock()

class Checker(threading.Thread):
    def __init__(self, application):
        threading.Thread.__init__(self) 
        self._application = application

    def run(self):
        print "checking now ..."
        handler = CommandUtility()
        
        server_access_ip = handler.get_access_ip( self._application.get_server().get_machine() )
        server_access_port = handler.get_access_port( self._application.get_server().get_machine() )
        cmd = handler.get_show_all_pid_cmd(server_access_ip, server_access_port)
        server_result = subprocess.check_output(cmd, shell=True)
        server_pid = self._application.get_server().get_program().get_pid()

        global is_running
        lock.acquire()
        if not (server_pid in server_result):
            name = self._application.get_server().get_program().get_name()
            print "The server of " + name + " is stop ..."
            client_access_ip = handler.get_access_ip( self._application.get_client().get_machine() )
            client_access_port = handler.get_access_port( self._application.get_client().get_machine() )
            cmd = handler.get_show_all_pid_cmd(client_access_ip, client_access_port)
            client_result = subprocess.check_output(cmd, shell=True)
            client_pid = self._application.get_client().get_program().get_pid()
            if client_pid in client_result:
                self._application.get_client().stop()
            is_running = False
        lock.release()


class SdnEmu:

    def __init__(self, rpinet):
        self._rpinet = rpinet
        self._start_queue = []
        self._stop_queue = []

    def addStartQueue(self, application):
        application.gen_server_cmd()
        application.gen_client_cmd()
        self._start_queue.append(application)

    def addStopQueue(self, application):
        self._stop_queue.append(application)

    def callChecker(self, application):
        print "generate a thread to check ..."
        while True:
            if not is_running:
                break
            Checker(application).start()
            time.sleep(60)

    def start(self):
        controllers = self._rpinet.get_controllers()
        for controller in controllers:
            controller.start()
        
        for application in self._start_queue:
            application.start_server()
            time.sleep(5)
            application.start_client()
            time.sleep(5)

        global is_running
        is_running = True

    def stop(self):
        global is_running
        if not is_running:
            for application in self._stop_queue:
                application.stop_server()
                time.sleep(5)
                application.stop_client()
                time.sleep(5)
            print "all applications are stop ..."
        else:
            print "emulation is still running ..."

        controllers = self._rpinet.get_controllers()
        for controller in controllers:
            controller.stop()

        switches = self._rpinet.get_switches()
        for switch in switches:
            switch.clear_table()

        print "PiSNet is stop!"
