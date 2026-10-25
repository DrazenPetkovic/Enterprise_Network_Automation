from netmiko import ConnectHandler
import getpass

# Note: The entire project was developed in this file in VS Code, but the debugging process was
# performed directly on the Automation container within GNS3. If you spot an error in this code,
# it has likely been resolved in the Automation container, but I may have forgotten to update it
# in this specific file.

class ConfigureNetwork:

    def __init__(self, device_type, host, username, password):
        self.device = {"device_type": device_type, "host": host, "username": username, "password": password}
        self.connect_to_device()

    def connect_to_device(self):
        try:
            self.connection = ConnectHandler(**self.device)
            print(f"SSH connection to {self.device['host']} is established")
            return True
        except Exception as e:
            print(f"Error: can't establish SSH connection with {self.device['host']}:")
            print(e)
            return False

    def enable_ip_routing(self):
        try:
            config_commands = ["ip routing"]
            output = self.connection.send_config_set(config_commands)
            print(f"{self.device['host']}: IP routing enabled")
            print(output)
        except Exception as e:
            print(f"{self.device['host']}: IP routing is NOT enabled")
            print(e)

    def disable_ip_routing(self):
        try:
            config_commands = ["no ip routing"]
            output = self.connection.send_config_set(config_commands)
            print(f"{self.device['host']}: IP routing disabled")
            print(output)

        except Exception as e:
            print(f"{self.device['host']}: IP routing NOT disabled")
            print(e)

    #For routers that acts like PCs
    def default_gateway(self, default_gateway):
        try:
            self.disable_ip_routing()
            config_commands = [f"ip default-gateway {default_gateway}"]
            output = self.connection.send_config_set(config_commands)
            print(f"{self.device['host']}: default gateway {default_gateway} is SET")
            print(output)
        except Exception as e:
            print(f"{self.device['host']}: default gateway {default_gateway} is NOT SET")
            print(e)

    def helper_address(self, file_name):
        try:
            config_commands = []
            file_lines = self.load_file_lines(file_name)
            for line in file_lines:
                interface, helper_address = line.split(":")
                config_command = [f"interface {interface}", f"ip helper-address {helper_address}"]
                config_commands.extend(config_command)
            output = self.connection.send_config_set(config_commands)
            print(f"{self.device['host']}: Helper address is set")
            print(output)

        except Exception as e:
            print(f"{self.device['host']}: Helper address is NOT set")
            print(e)


    def dhcp_interface(self, interface):
        try:
            config_commands = [f"interface {interface}", "ip address dhcp", "no shut"]
            output = self.connection.send_config_set(config_commands)
            print(f"{self.device['host']}: This host is DHCP Client")
            print(output)
        except Exception as e:
            print(f"{self.device['host']}: This host CAN'T be DHCP Client")
            print(e)

    # Kompletirano
    def configure_acl(self, file_name):
        try:
            file_lines = self.load_file_lines(file_name)
            output = self.connection.send_config_set(file_lines)
            print(f"{self.device['host']}: ACL is successfuly created")
            print(output)
        except Exception as e:
            print(f"{self.device['host']}: ACL is NOT created")
            print(e)

    def load_file_lines(self,file_name):
        try:
            file_lines = []
            with open(file_name, "r") as file:
                for line in file:
                    file_lines.append(line.strip())

            return file_lines
        except Exception as e:
            print(f"{self.device['host']}: Can't open file {file_name}")
            print(e)

    def read_network_mappings(self, file_name):
        try:
            file_list = self.load_file_lines(file_name)
            full_list = []
            for index in range(len(file_list) - 1):
                dict_list = {}
                if index % 2 == 0 or index == 0:
                    dict_list[file_list[index]] = file_list[index + 1]
                full_list.append(dict_list)
            return full_list


        except Exception as e:
            print(e)

    def nat_direction(self, int_id, direction):
        try:
            config_commands = [f"int {int_id}", f"ip nat {direction}"]
            output = self.connection.send_config_set(config_commands)
            print(f"{self.device['host']}: {int_id} is NAT {direction} interface")
            print(output)
        except Exception as e:
            print(f"{self.device['host']}: {int_id} is NOT NAT {direction} interface")
            print(e)

    def set_default_gateway(self, ip_address):
        try:
            config_commands = [f"ip default-gateway {ip_address}"]
            output = self.connection.send_config_set(config_commands)
            print(output)
            print(f"{ip_address} is default gateway for {self.device['host']}")
        except Exception as e:
            print(f"{ip_address} is NOT default gateway for {self.device['host']}")
            print(e)


    #Kompletirano
    def load_vlans_from_file(self, file_name):
        try:
            vlan_list = self.load_file_lines(file_name)
            for vlan in vlan_list:
                vlan_id, vlan_name = vlan.split(":")
                config_commands = [f"vlan {vlan_id}", f"name {vlan_name}"]
                output = self.connection.send_config_set(config_commands)
                print(output)
        except Exception as e:
            print(f"{self.device['host']}: Can't load {file_name}")
            print(e)

    # Kompletirano
    def remove_vlans(self, file_name):
        try:
            file_data = self.load_file_lines(file_name)
            config_commands = []
            for vlan in file_data:
                config_commands.append(f"no vlan {vlan}")
            output = self.connection.send_config_set(config_commands)
            print(f"{self.device['host']}: vlans are successfully removed")
            print(output)

        except Exception as e:
            print(f"{self.device['host']}: vlans are NOT removed")
            print(e)

    # Kompletirano
    def configure_trunk(self, file_name):
        try:
            file_lines = self.load_file_lines(file_name)
            config_commands = []
            for line in file_lines:
                interface, vlans = line.split(":")
                commands = [f"interface {interface}", "switchport trunk encapsulation dot1q",
                "switchport mode trunk", f"switchport trunk allowed vlan {vlans}"]
                config_commands.extend(commands)
                    
            output = self.connection.send_config_set(config_commands)
            print(f"{self.device['host']}: Trunk is successfully configured")
            print(output)
        except Exception as e:
            print(f"{self.device['host']}: Trunk is NOT configured!")
            print(e)

    #Kompletirano
    def configure_ospf(self, file_name):
        try:
            config_commands = []
            file_lines = self.load_file_lines(file_name)
            for line in file_lines:
                interface, process_id, area_id = line.split(":")
                config_command = [f"interface {interface}", f"ip ospf {process_id} area {area_id}"]
                config_commands.extend(config_command)

            output = self.connection.send_config_set(config_commands)
            print(f"{self.device['host']}: OSPF is successfully configured!")
            print(output)
        except Exception as e:
            print(f"{self.device['host']}: OSPF is NOT successfully configured")
            print(e)

    # Kompletirano
    def ospf_passive_interfaces(self, file_name):
        try:
            config_commands = []
            file_lines = self.load_file_lines(file_name)
            for line in file_lines:
                process_id, interface = line.split(":")
                config_command = [f"router ospf {process_id}", f"passive-interface {interface}"]
                config_commands.extend(config_command)
            output = self.connection.send_config_set(config_commands)
            print(f"{self.device['host']}: passive interface operation success")
            print(output)

        except Exception as e:
            print(f"{self.device['host']}: passive interface operation interrupted")
            print(e)

    # Kompletirano
    def create_etherchannel(self, file_name):
        try:
            file_lines = self.load_file_lines(file_name)
            config_commands = []
            for line in file_lines:
                group_number, interfaces, mode = line.split(":")
                modified_interfaces = interfaces.replace(",", ", ")
                config_command = [f"interface range {modified_interfaces}", f"channel-group {group_number} mode {mode}"]
                config_commands.extend(config_command)
            output = self.connection.send_config_set(config_commands)
            print(f"{self.device['host']}: Etherchannel is successfully created")
            print(output)
        except Exception as e:
            print(f"{self.device['host']}: Etherchannel is NOT successfully created")
            print(e)

    # Kompletirano
    def configure_dhcp(self, file_name):
        try:
            file_lines = self.load_file_lines(file_name)
            config_commands = []
            for line in file_lines:
                pool_name, ip_address, subnet_mask, default_router, dns_server = line.split(":")
                config_command = [f"ip dhcp pool {pool_name}", f"network {ip_address} {subnet_mask}",
                f"default-router {default_router}", f"dns-server {dns_server}"]
                config_commands.extend(config_command)
            output = self.connection.send_config_set(config_commands)
            print(f"{self.device['host']}: DHCP is successfully configured")
            print(output)
        except Exception as e:
            print(f"{self.device['host']}: DHCP is NOT successfully configured")
            print(e)

    # Kompletirano
    def dhcp_excluded_addresses(self, file_name):
        try:
            file_lines = self.load_file_lines(file_name)
            config_commands = []
            for line in file_lines:
                if ":" in line:
                    first_addr, last_addr = line.split(":")
                    config_command = f"ip dhcp excluded-address {first_addr} {last_addr}"
                    config_commands.append(config_command)
                else:
                    config_command = f"ip dhcp excluded-address {line}"
                    config_commands.append(config_command)

            output = self.connection.send_config_set(config_commands)
            print(f"{self.device['host']}: All addresses are excluded")
            print(output)

        except Exception as e:
            print(f"{self.device['host']}: Error: addresses can't be excluded")
            print(e)

    #Kompletirano
    def map_ports_to_vlan(self, file_name):
        try:
            file_lines = self.load_file_lines(file_name)
            config_commands = []
            for line in file_lines:
                vlan, interfaces = line.split(":")
                if "," in interfaces:
                    modified_interfaces = interfaces.replace(",", ", ")
                    command = [f"interface range {modified_interfaces}", "switchport mode access", f"switchport access vlan {vlan}"]
                    config_commands.extend(command)
                else:
                    command = [f"interface {interfaces}", "switchport mode access", f"switchport access vlan {vlan}"]
                    config_commands.extend(command)
            output = self.connection.send_config_set(config_commands)
            print(f"{self.device['host']}: All interfaces are mapped")
            print(output)
        except Exception as e:
            print(f"{self.device['host']}: mapping interfaces interrupted")
            print(e)

    #Kompletirano
    def config_ip_from_file(self, file_name):
        try:
            file_lines = self.load_file_lines(file_name)
            config_commands = []
            for line in file_lines:
                interface, ip_address, subnet_mask = line.split(":")
                config_command = [f"interface {interface}", f"ip address {ip_address} {subnet_mask}", "no shut"]
                config_commands.extend(config_command)
            output = self.connection.send_config_set(config_commands)
            print(f"{self.device['host']}: IP address successfully configured")
            print(output)
        except Exception as e:
            print(f"{self.device['host']}: IP address is NOT configured")
            print(e)

    def config_routed_port(self, file_name):
        try:
            file_lines = self.load_file_lines(file_name)
            config_commands = []
            for line in file_lines:
                interface, ip_address, subnet_mask = line.split(":")
                config_command = [f"interface {interface}", "no switchport", f"ip address {ip_address} {subnet_mask}", "no shut"]
                config_commands.extend(config_command)
                output = self.connection.send_config_set(config_commands)
                print(f"{self.device['host']}: IP address successfully configured")
                print(output)
        except Exception as e:
            print(f"{self.device['host']}: IP address is NOT configured")
            print(e)
        

    #Kompletirano
    def configure_nat(self, file_name):
        try:
            file_lines = self.load_file_lines(file_name)
            config_commands = []
            for line in file_lines:
                acl_name, interface_id = line.split(":")
                config_command = [f"ip nat inside source list {acl_name} interface {interface_id} overload"]
                config_commands.extend(config_command)
            output = self.connection.send_config_set(config_commands)
            print(f"{self.device['host']}: NAT is successfully configured")
            print(output)
        except Exception as e:
            print(f"{self.device['host']}: NAT is NOT configured")
            print(e)

    def configure_dns(self, file_name):
        try:
            file_lines = self.load_file_lines(file_name)
            config_commands = ["ip dns server"]
            for line in file_lines:
                domain, ip_address = line.split(":")
                config_command = [f"ip host {domain} {ip_address}"]
                config_commands.extend(config_command)
            output = self.connection.send_config_set(config_commands)
            print(f"{self.device['host']}: DNS Server is configured")
            print(output)
        except Exception as e:
            print(f"{self.device['host']}: DNS Server is NOT configured")
            print(e)

    def apply_acls(self, file_name):
        try:
            file_lines = self.load_file_lines(file_name)
            config_commands = []
            for line in file_lines:
                interface, acl_name, direction = line.split(":")
                config_command = [f"interface {interface}", f"ip access-group {acl_name} {direction}"]
                config_commands.extend(config_command)
            output = self.connection.send_config_set(config_commands)
            print(f"{self.device['host']}: ACL applied to an interface")
            print(output)
        except Exception as e:
            print(f"{self.device['host']}:ACL NOT applied to an interface")
            print(e)

    def nat_direction(self, file_name):
        try:
            file_lines = self.load_file_lines(file_name)
            config_commands = []
            for line in file_lines:
                interface, direction = line.split(":")
                config_command = [f"interface {interface}", f"ip nat {direction}"]
                config_commands.extend(config_command)
            output = self.connection.send_config_set(config_commands)
            print(f"{self.device['host']}: NAT direction is SET")
            print(output)
        except Exception as e:
            print(f"{self.device['host']}: NAT direction is NOT SET")
            print(e)

    def enable_web_service(self):
        try:
            config_commands = ["ip http server", "ip http secure-server"]
            output = self.connection.send_config_set(config_commands)
            print(f"{self.device['host']}: HTTP and HTTPS are ENABLED")
            print(output)
        except Exception as e:
            print(f"{self.device['host']}: HTTP and HTTPS are NOT ENABLED")
            print(e)
    



# Testing

if __name__ == "__main__":
    password = getpass.getpass()
    path = r"C:\Users\Administrator\Desktop\Python Files\configs\interface_mappings_config"

    device_orchestrator = {
        #SW1
        "192.168.0.5": {
            "vlans":"configs/vlan_config/sw1_vlans.txt",
            "vlan_map":"configs/interface_mappings_config/sw1_vlan_ports.txt",
            "label":"L3Switch",
            "ip_config":"configs/ip_config/sw1_ips.txt",
            "switchport_config":"configs/ip_config/sw1_physical.txt",
            "ospf_config":"configs/ospf_config/sw1_ospf.txt",
            "ospf_passive_interfaces":"configs/ospf_config/sw1_ospf_passive_interfaces.txt",
            "acl_config":"configs/acl_config/create_acls.txt",
            "acl_apply":"configs/acl_config/apply_acls.txt",
            "helper_address":"configs/dhcp_config/sw1_helper_address.txt"
        },
        #SW2
        "192.168.0.8": {
            "vlans":"configs/vlan_config/sw2_vlans.txt",
            "vlan_map":"configs/interface_mappings_config/sw2_vlan_ports.txt",
            "etherchannel":"configs/etherchannel_config/sw2_etherchannel.txt",
            "trunk_interface":"configs/trunk_config/allowed_vlans.txt",
            "label":"L3Switch",
            "ip_config":"configs/ip_config/sw2_ips.txt",
            "switchport_config":"configs/ip_config/sw2_physical.txt",
            "ospf_config":"configs/ospf_config/sw2_ospf.txt",
            "ospf_passive_interfaces":"configs/ospf_config/sw2_ospf_passive_interfaces.txt",
            "helper_address":"configs/dhcp_config/sw2_helper_address.txt"
        },
        #SW3
        "192.168.0.9": {
            "vlans":"configs/vlan_config/sw3_vlans.txt",
            "vlan_map":"configs/interface_mappings_config/sw3_vlan_ports.txt",
            "etherchannel":"configs/etherchannel_config/sw3_etherchannel.txt",
            "trunk_interface":"configs/trunk_config/allowed_vlans.txt",
	    "label":"L3Switch",
            "ip_config":"configs/ip_config/sw3_ips.txt",
            "ospf_config":"configs/ospf_config/sw3_ospf.txt",
            "ospf_passive_interfaces":"configs/ospf_config/sw3_ospf_passive_interfaces.txt"
        },
        #PC1
        "192.168.0.1": {
            "default_gateway":"192.168.10.254",
            "dhcp_interface":"g0/1"
        },
        #PC2
        "192.168.0.2": {
            "default_gateway": "192.168.20.254",
            "dhcp_interface":"g0/1"
        },
        #PC3
        "192.168.0.3": {
            "default_gateway": "192.168.10.254",
            "dhcp_interface":"g0/1"
        },
        #PC4
        "192.168.0.4": {
            "default_gateway": "192.168.20.254",
            "dhcp_interface":"g0/1"
        },
        #R1
        "192.168.0.6": {
            "ip_config":"configs/ip_config/r1_ips.txt",
            "ospf_config":"configs/ospf_config/r1_ospf.txt",
            "nat_direction":"configs/nat_config/nat_direction.txt",
            "acl_config":"configs/nat_config/nat_acl.txt",
            "nat_config":"configs/nat_config/nat_overload.txt"
        },
        #R2
        "192.168.0.7": {
            "ip_config":"configs/ip_config/r2_ips.txt",
            "ospf_config":"configs/ospf_config/r2_ospf.txt"
        },
        #DHCP&DNSServer
        "192.168.0.10": {
            "default_gateway": "10.0.30.254",
            "ip_config":"configs/ip_config/dhcp_ips.txt",
            "dhcp_excluded":"configs/dhcp_config/dhcp_excluded_addresses.txt",
            "dhcp_configuration":"configs/dhcp_config/configure_dhcp.txt",
            "dns_configuration":"configs/dns_config/dns_config.txt",
        },
        #WEBServer1
        "192.168.0.11": {
            "default_gateway": "10.0.40.254",
            "ip_config": "configs/ip_config/web_server_1.txt",
            "enable_web": "enable_web_services"
        },
        #WEBServer2
        "192.168.0.12": {
            "default_gateway": "10.0.50.254",
            "ip_config": "configs/ip_config/web_server_2.txt",
            "enable_web": "enable_web_services"
        }
    }

    sw1 = {
        "device_type":"cisco_ios",
        "host":"192.168.0.5",
        "username":"drazen",
        "password": password
    }
    sw2 = {
        "device_type":"cisco_ios",
        "host":"192.168.0.8",
        "username":"drazen",
        "password": password
    }
    sw3 = {
        "device_type":"cisco_ios",
        "host":"192.168.0.9",
        "username":"drazen",
        "password": password
    }
    pc1 = {
        "device_type": "cisco_ios",
        "host":"192.168.0.1",
        "username":"drazen",
        "password": password
    }
    pc2 = {
        "device_type": "cisco_ios",
        "host": "192.168.0.2",
        "username": "drazen",
        "password": password
    }
    pc3 = {
        "device_type": "cisco_ios",
        "host": "192.168.0.3",
        "username": "drazen",
        "password": password
    }
    pc4 = {
        "device_type": "cisco_ios",
        "host": "192.168.0.4",
        "username": "drazen",
        "password": password
    }
    r1 = {
        "device_type": "cisco_ios",
        "host": "192.168.0.6",
        "username": "drazen",
        "password": password
    }
    r2 = {
        "device_type": "cisco_ios",
        "host": "192.168.0.7",
        "username": "drazen",
        "password": password
    }
    dhcp = {
        "device_type":"cisco_ios",
        "host":"192.168.0.10",
        "username":"drazen",
        "password": password
    }
    web_server_1 = {
        "device_type": "cisco_ios",
        "host": "192.168.0.11",
        "username": "drazen",
        "password": password
    }
    web_server_2 = {
        "device_type": "cisco_ios",
        "host": "192.168.0.12",
        "username": "drazen",
        "password": password
        }

    devices_list = [sw1, sw2, sw3, pc1, pc2, pc3, pc4, r1, r2, dhcp, web_server_1, web_server_2]

    for device in devices_list:
        device_ip = device['host']
        config_net = ConfigureNetwork(**device)
        if device_ip in device_orchestrator:
            tasks = device_orchestrator[device_ip]
            print(f"Configuring device #####{device_ip}#####")
            if "vlans" in tasks:
                config_net.load_vlans_from_file(tasks["vlans"])
            if "vlan_map" in tasks:
                config_net.map_ports_to_vlan(tasks["vlan_map"])
            if "etherchannel" in tasks:
                config_net.create_etherchannel(tasks["etherchannel"])
            if "trunk_interface" in tasks:
                config_net.configure_trunk(tasks["trunk_interface"])
            if "switchport_config" in tasks:
                config_net.config_routed_port(tasks["switchport_config"])
            if "ip_config" in tasks:
                config_net.config_ip_from_file(tasks["ip_config"])
            if "ospf_config" in tasks:
                config_net.configure_ospf(tasks["ospf_config"])
            if "ospf_passive_interfaces" in tasks:
                config_net.ospf_passive_interfaces(tasks["ospf_passive_interfaces"])
            if "label" in tasks:
                config_net.enable_ip_routing()
            if "default_gateway" in tasks:
                config_net.default_gateway(tasks["default_gateway"])
            if "helper_address" in tasks:
                config_net.helper_address(tasks["helper_address"])
            if "dhcp_interface" in tasks:
                config_net.dhcp_interface(tasks["dhcp_interface"])
            if "dhcp_excluded" in tasks:
                config_net.dhcp_excluded_addresses(tasks["dhcp_excluded"])
            if "dhcp_configuration" in tasks:
                config_net.configure_dhcp(tasks["dhcp_configuration"])
            if "dns_configuration" in tasks:
                config_net.configure_dns(tasks["dns_configuration"])
            if "acl_config" in tasks:
                config_net.configure_acl(tasks["acl_config"])
            if "acl_apply" in tasks:
                config_net.apply_acls(tasks["acl_apply"])
            if "nat_direction" in tasks:
                config_net.nat_direction(tasks["nat_direction"])
            if "nat_config" in tasks:
                config_net.configure_nat(tasks["nat_config"])
            if "enable_web" in tasks:
                config_net.enable_web_service()



        config_net.connection.disconnect()
