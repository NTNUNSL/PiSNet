from utility import CommandUtility

class Program:

    def __init__(self):
        self._name = ""
        self._cmd = ""
        self._pid = ""

    def get_name(self):
        return self._name

    def get_cmd(self):
        return self._cmd

    def get_pid(self):
        return self._pid

    def set_name(self, name):
        self._name = name

    def set_cmd(self, cmd):
        self._cmd = cmd

    def set_pid(self, pid):
        self._pid = pid


class Application(object):

    def __init__(self, application):

        from node import RpiHost

        self._application = application
        self._server_remote_cmd = ""
        self._client_remote_cmd = ""
        self._server = RpiHost()
        self._client = RpiHost()
        self._mapping_table = {}
        self._handler = CommandUtility()

    def setServer(self, rpi_host, remote_cmd):
        machine = rpi_host.get_machine()
        machine_content = machine.values().pop()
        self._server_remote_cmd = self._handler.replace(remote_cmd, machine_content)
        key = self._handler.get_server_ip_variable()
        self._mapping_table[key] = self._handler.get_host_ip(machine)
        self._server.clone(rpi_host)
        self._server.set_program_name( self._handler.get_program_name(self._application) )

    def setClient(self, rpi_host, remote_cmd):
        machine = rpi_host.get_machine()
        machine_content = machine.values().pop()
        self._client_remote_cmd = self._handler.replace(remote_cmd, machine_content)
        key = self._handler.get_client_ip_variable()
        self._mapping_table[key] = self._handler.get_host_ip(machine)
        self._client.clone(rpi_host)
        self._client.set_program_name( self._handler.get_program_name(self._application) )

    def setLogNo(self, number):
        key = self._handler.get_log_no_variable()
        self._mapping_table[key] = str(number)

    def get_server(self):
        return self._server

    def get_client(self):
        return self._client

    def gen_server_cmd(self):
        server_exec_cmd = self._handler.get_app_server_cmd(self._application)
        exec_cmd = self._handler.replace(server_exec_cmd, self._mapping_table)
        server_exec_cmd = self._server_remote_cmd + " " + exec_cmd
        self._server.set_program_cmd(server_exec_cmd)

    def gen_client_cmd(self):
        client_exec_cmd = self._handler.get_app_client_cmd(self._application)
        exec_cmd = self._handler.replace(client_exec_cmd, self._mapping_table)
        client_exec_cmd = self._client_remote_cmd + " " + exec_cmd
        self._client.set_program_cmd(client_exec_cmd)

    def start_server(self):
        self._server.start()

    def start_client(self):
        self._client.start()

    def stop_server(self):
        self._server.stop()

    def stop_client(self):
        self._client.stop()


