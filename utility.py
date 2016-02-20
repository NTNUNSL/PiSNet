import ConfigParser
import re
import subprocess

class ConfigUtility:
    
    def __init__(self):
        self._config = None
            
    def read(self, config_file):
        self._config = ConfigParser.ConfigParser()
        self._config.read(config_file)

    def get(self, section, option=''):
        if option != '':
            return self._config.get(section, option)
        else:
            attributes = self._config.options(section)
            properties = {}
            for index in xrange( len(attributes) ):
                variable = "${" + attributes[index] + "}"
                properties[variable] = self._config.get(section, attributes[index])
                hash_table = {}
                hash_table[section] = properties
            return hash_table


class CommandUtility:

    def _get_remote_cmd(self, ip, port):
        return "ssh pi@" + ip + " -p " + port

    def get_search_process_cmd(self, ip, port, program):
        return self._get_remote_cmd(ip, port) + " pidof " + program
    
    def get_kill_process_cmd(self, ip, port, pid):
        return self._get_remote_cmd(ip, port) + " sudo kill " + pid
    
    def get_show_all_pid_cmd(self, ip, port):
        return self._get_remote_cmd(ip, port) + " ps -o pid"

    def get_clear_table_cmd(self, ip, port):
        return self._get_remote_cmd(ip, port) + " sudo ovs-ofctl del-flows ovs-br1 -O openflow13"

    def get_switch_dpid(self, ip, port):
        cmd = self._get_remote_cmd(ip, port) + " ip link show ovs-br1"
        result = subprocess.check_output(cmd, shell=True)
        pattern = "\w\w:\w\w:\w\w:\w\w:\w\w:\w\w"
        match = re.search(pattern, result)
        mac_str = match.group().replace(':','').lstrip('0')
        mac_address = int(mac_str, 16)
        return str(mac_address)

    def get_access_ip(self, machine):
        machine_content = machine.values().pop()
        return  machine_content.get('${manager}')

    def get_access_port(self, machine):
        machine_content = machine.values().pop()
        return  machine_content.get('${access_port}')

    def get_host_ip(self, machine):
        machine_content = machine.values().pop()
        return  machine_content.get('${ip}')

    def get_program_name(self, application):
        application_content = application.values().pop()
        return application_content.get('${program}')

    def get_controller_service(self, application):
        application_content = application.values().pop()
        return application_content.get('${service}')
    
    def get_app_server_cmd(self, application):
        application_content = application.values().pop()
        return application_content.get('${server}')

    def get_app_client_cmd(self, application):
        application_content = application.values().pop()
        return application_content.get('${client}')

    def get_server_ip_variable(self):
        return "${server_ip}"

    def get_client_ip_variable(self):
        return "${client_ip}"

    def get_log_no_variable(self):
        return "${no}"

    def replace(self, cmd, mapping_table):
        pattern = "\$\{\w+\}"
        matches = re.findall(pattern, cmd)
        for cmd_variable in matches:
            cmd = cmd.replace( cmd_variable, mapping_table.get(cmd_variable) )
        return cmd


