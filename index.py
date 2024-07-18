import subprocess
import json
import http.client
from helper import *

class LldpCollector:
    """
    This class collects LLDP information and interacts with an API.
    """

    def __init__(self, server_url: str, api_endpoint: str):
        self.server_url = server_url
        self.api_endpoint = api_endpoint
        self.command_chassis = "sudo lldpcli -f json0 show chassis"
        self.command_neighbors = "sudo lldpcli -f json0 show neighbors"

    def run_lldpcli_command(self, command):
        """
        Runs the lldpcli command and captures the output.

        Args:
            command: The command to be executed.

        Returns:
            The output of the command as a string, or None if an error occurs.
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error running command: {e}")
            print(f"Output: {e.output}")
            print(f"Error Output: {e.stderr}")
            return None

    def create_dict(self, chassis, neighbor):
        """
        Creates a dictionary with structured information from lldp output.

        Args:
            chassis_data: JSON data for the local chassis.
            neighbor_data: JSON data for neighboring devices.

        Returns:
            A dictionary containing chassis and neighbor information.
        """
        info = {"chassis": None, "neighbor": []}

        try:
            #code for chassis information
            temp_dict = {}
            checked_data = deep_get(chassis,['local-chassis',0,'chassis',0])

            if checked_data:
                temp_dict['node_id'] = deep_get(checked_data,['id',0,'value'])
                temp_dict['node_id_type'] = deep_get(checked_data,['id',0,'type'])
                temp_dict['sys_name'] = deep_get(checked_data,['name',0,'value'])
                temp_dict['sys_description'] = deep_get(checked_data,['descr',0,'value'])
                temp_dict['mgmt_ip'] = deep_get(checked_data,['mgmt-ip',0,'value'])
                temp_dict['capability'] = {
                    'Bridge': False, 
                    'Router': False, 
                    'Wlan': False, 
                    'Station': False
                }
                
                if ("capability" in checked_data) and checked_data['capability']:
                    for capabilities in checked_data['capability']:
                        temp_dict['capability'][capabilities['type']] = capabilities['enabled']
            
                info['chassis'] = temp_dict
        
            # Code for neighbor information
            checked_data = deep_get(neighbor, ['lldp',0,'interface'])

            if checked_data:
                for neighbor in checked_data:
                    temp_dict = {}
                    chassis_info = deep_get(neighbor, ['chassis', 0])
                    port_info = deep_get(neighbor, ['port', 0])
                    temp_dict['interface'] = deep_get(neighbor, ['name'])
                    temp_dict['neighbor_id'] = deep_get(chassis_info, ['id', 0, 'value'])
                    temp_dict['neighbor_id_type'] = deep_get(chassis_info, ['id', 0, 'type'])
                    temp_dict['name'] = deep_get(chassis_info, ['name', 0, 'value'])
                    temp_dict['mgmt_ip'] = deep_get(chassis_info, ['mgmt-ip', 0, 'value'])
                    temp_dict['port_id_type'] = deep_get(port_info, ['id', 0, 'type'])
                    temp_dict['port_id'] = deep_get(port_info, ['id', 0, 'value'])
                    temp_dict['port_description'] = deep_get(port_info, ['descr', 0, 'value'])
                    temp_dict['port_ttl'] = deep_get(port_info, ['ttl', 0, 'value'])
                    temp_dict['capability'] = {
                        'Bridge': False, 
                        'Router': False, 
                        'Wlan': False, 
                        'Station': False
                    }

                    if ("capability" in chassis_info) and chassis_info['capability']:
                        for capabilities in chassis_info['capability']:
                            temp_dict['capability'][capabilities['type']] = capabilities['enabled']

                    info['neighbor'].append(temp_dict)
        except Exception as e:
            #code
            print(type(e))
            print(f"Error running command: {e}")
        finally:
            return info

    def _make_api_request(self, data):
        """
        Makes a POST request to the server with the provided data.

        Args:
            data: The data to be sent to the server (dictionary).

        Returns:
            The JSON response from the server, or None if an error occurs.
        """
        try:
            headers = {"Content-type": "application/json; charset=UTF-8"}
            connection = http.client.HTTPConnection(self.server_url)

            post_data = json.dumps(data)
            connection.request("POST", self.api_endpoint, body=post_data, headers=headers)

            response = connection.getresponse()
            data = response.read().decode("utf-8")
            json_data = json.loads(data)
            connection.close()

            return json_data
        except Exception as e:
            print(f"An error occurred in the API call: {e}")
            return None

    def collect_and_send(self):
        """
        Collects LLDP information, creates a dictionary, and sends it to the server.

        Returns:
            The server's response data as a dictionary, or None if an error occurs.
        """

        chassis_output = self.run_lldpcli_command(self.command_chassis)
        neighbor_output = self.run_lldpcli_command(self.command_neighbors)

        if chassis_output and neighbor_output:
            json_chassis = json.loads(chassis_output)
            json_neighbors = json.loads(neighbor_output)
            data = self.create_dict(json_chassis, json_neighbors)
            return self._make_api_request(data)

        return None


# Example usage
collector = LldpCollector("10.0.0.1:9000", "/lldp")
response_data = collector.collect_and_send()

if response_data:
    print("API response data:", response_data)
