# Ansible Playbooks

Contains all playbooks created for small tasks

1. collect-data<br />
-collect_in_one_file.yml: Runs cmds and stores output in one separate file (using templates)<br />
-collect_in_separate_files.yml: Runs cmds and stores output of commands in separate files<br />

2. backup_configs<br />
-backup_with_cmd_mod.yml: Backup ASAs, IOS and NXOS using Ansible command modules in seperate plays<br />
-backup_with_napalm.yml: Backup ASAs, IOS and NXOS using napalm and F5 using bigip module<br />

3. cloud_vpn<br />
-playbook_cloud_vpn.yml: Build a site-to-site VPN between Azure and a Cisco ASA5505

4. create_vlan<br />
-playbook_create_vlans.yml: Build and verify VLANs on IOS

5. network_state_report<br />
-playbook_main.yml: Generates tables of device state (asa, nxos, ios, bigip) for network elements (Interfaces, MACs, ARPs, VPN, OSPF, BGP) and builds a report
