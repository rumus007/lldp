## Pre-requisites

* Python >= v3.9
* LLDPD library https://lldpd.github.io/

## About The Project

This program is written in Python and uses the LLDPD library which utilizes the LLDP protocol to collect information about the current device and its neighbors and calls the endpoint of Ground-control to store the data

## Getting started

* Clone the repository into the required nodes or the virtual machine
* Make sure the endpoint in the index.py file is correct. Right now it is at localhost:9000
* Run the command ```python3 index.py``` to execute the command.