## Pre-requisites

* Python >= v3.9
* LLDPD library https://lldpd.github.io/

## About The Project

This program is written in Python and uses the LLDPD library which utilizes the LLDP protocol to collect information about the current device and its neighbors and calls the endpoint of Ground-control to store the data

## Getting started

* Clone the repository into the required nodes or the virtual machine
* Copy the .env.example file into .env file.
* Make sure the endpoint in the .env file is correct. Right now it is at 10.0.0.1:9000
* Run the command ```python3 index.py``` to execute the command.