import subprocess
import json
import http.client
from helper import *

def run_lldpcli_command(command):
    """
    Runs the lldpcli command to get self and neighbor information

    Parameters:
    - command: The cli command to be runned

    Returns:
    - The value if found, otherwise None.
    """
    try:
        # Run the command and capture the output
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

def create_dict(chassis, neighbor):
    """
    Creates a dictionary of the information provided for storage

    Parameters:
    - chassis: JSON data for chassis from the CLI command
    - neighbor: JSON data for neighbor from the CLI command

    Returns:
    - The the dictionary value
    """
    info = { "chassis": None, "neighbor": [] }

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
            temp_dict['capability'] = {}
            
            if checked_data['capability']:
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
                temp_dict['neigbor_id'] = deep_get(chassis_info, ['id', 0, 'value'])
                temp_dict['neigbor_id_type'] = deep_get(chassis_info, ['id', 0, 'type'])
                temp_dict['name'] = deep_get(chassis_info, ['name', 0, 'value'])
                temp_dict['mgmt_ip'] = deep_get(chassis_info, ['mgmt-ip', 0, 'value'])
                temp_dict['port_id_type'] = deep_get(port_info, ['id', 0, 'type'])
                temp_dict['port_id'] = deep_get(port_info, ['id', 0, 'value'])
                temp_dict['port_description'] = deep_get(port_info, ['descr', 0, 'value'])
                temp_dict['port_ttl'] = deep_get(port_info, ['ttl', 0, 'value'])
                temp_dict['capability'] = {}

                if chassis_info['capability']:
                    for capabilities in chassis_info['capability']:
                        temp_dict['capability'][capabilities['type']] = capabilities['enabled']

                info['neighbor'].append(temp_dict)

        return info

    except Exception as e:
        #code
        print(type(e))
        print(f"Error running command: {e}")

def api_call(data):
    """
    API POST request to server to store the lldp data

    Parameters:
    - data: Dictionary that contains the data of chassis and neighbors 

    Returns:
    - HTTP response from the server
    """
    try:
        # Code
        host = "postman-echo.com"
        endpoint = "/post"

        post_data = json.dumps(data)

        headers = {
            "Content-type": "application/json; charset=UTF-8"
        }

        connection = http.client.HTTPSConnection(host)

        connection.request("POST", endpoint, body=post_data, headers=headers)

        response = connection.getresponse()

        data = response.read()

        decode_data = data.decode("utf-8")

        json_data = json.loads(decode_data)

        connection.close()

        return json_data
    except Exception as e:
        print(f"An error has occured in API call: {e}")

# Command to run local chassis information
command_chassis = "sudo lldpcli -f json0 show chassis"

# Command to run neighbor information
command_neighbors = "sudo lldpcli -f json0 show neighbors"

# Run the command and get the output
output_chassis = run_lldpcli_command(command_chassis)
output_neighbors = run_lldpcli_command(command_neighbors)


if output_chassis:
    json_output_chassis = json.loads(output_chassis)
    json_output_neighbors = json.loads(output_neighbors)
    api_request = create_dict(json_output_chassis, json_output_neighbors)
    api_response = api_call(api_request)
    print("here", api_response['data'])
