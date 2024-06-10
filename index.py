import subprocess
import json
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

def create_dict(data):
    """
    Creates a dictionary of the information provided for storage

    Parameters:
    - data: JSON data from the CLI command

    Returns:
    - The the dictionary value
    """
    temp_dict = {
        'node_mac': '',
        'sys_name': '',
        'sys_description': '',
        'mgmt_ip': '',
        'capability': {
            'Bridge': False,
            'Router': False,
            'Wlan': False,
            'Station': False
        },
    }

    try:
        #code
        checked_data = deep_get(data,['local-chassis',0,'chassis',0])

        if checked_data:
            temp_dict['node_mac'] = deep_get(checked_data,['id',0,'value'])
            temp_dict['sys_name'] = deep_get(checked_data,['name',0,'value'])
            temp_dict['sys_description'] = deep_get(checked_data,['descr',0,'value'])
            temp_dict['mgmt_ip'] = deep_get(checked_data,['mgmt-ip',0,'value'])
            
            if checked_data['capability']:
                for capabilities in checked_data['capability']:
                    temp_dict['capability'][capabilities['type']] = capabilities['enabled']
    except Exception as Err:
        #code
        print(type(Err))

    return temp_dict

# Command to run local chassis information
command = "sudo lldpcli -f json0 show chassis"

# Run the command and get the output
output = run_lldpcli_command(command)

if output:
    json_output = json.loads(output)
    test = create_dict(json_output)
    print(test)