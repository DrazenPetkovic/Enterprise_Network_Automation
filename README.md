# Enterprise Network Automation with Python & Netmiko

![Network Topology](Topology.jpg)

## Project Overview
This repository contains an end-to-end network automation project developed to configure and manage a complex Cisco enterprise network environment simulated in GNS3. The core of this project is a robust, Object-Oriented Python script (`ConfigureNetwork.py`) utilizing the `netmiko` library to push configurations to multiple routing and switching devices dynamically. 

This project demonstrates scalable infrastructure management by separating Python logic from configuration data, ensuring a clean and modular architecture.

## Technologies & Tools
* **Programming:** Python 3
* **Libraries:** Netmiko (SSH connection handling)
* **Simulation Environment:** GNS3 (Cisco IOU/vIOS images, Docker Automation Container, VPCS)
* **Design Pattern:** Object-Oriented Programming (OOP)

## Automated Network Features
* VLAN Configuration and Inter-VLAN Routing
* OSPF Dynamic Routing & Passive Interfaces
* DHCP Server Provisioning
* Access Control Lists (ACLs) for security
* Network Address Translation (NAT)
* EtherChannel and 802.1Q Trunking

## Repository Structure
* `ConfigureNetwork.py`: The main OOP automation script containing the execution logic.
* `configs/`: Directory containing modular text files for device-specific configurations.
* `Documentation/`: Additional project documentation and device notes.
* `Topology.jpg`: Visual representation of the network architecture.

## Deployment Notes
* **Spanning Tree Protocol (STP) Convergence:** PortFast is not explicitly configured on edge ports in this specific lab. After booting the full GNS3 topology, it is highly recommended to wait at least one minute for STP to converge before executing the Python script.
* **Separation of Concerns:** The script dynamically reads network commands from the `configs/` directory, allowing for easy updates to network parameters without modifying the core Python code.

## Video Demonstration
*[Video presentation link will be added here]*
