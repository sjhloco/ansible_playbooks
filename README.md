# Ansible Playbooks

Contains all playbooks created for small tasks

1. collect-data \
    \- *collect_in_one_file.yml*: Runs cmds and stores output in one separate file (using templates) \
    \- *collect_in_separate_files.yml*: Runs cmds and stores output of commands in separate files

2. backup_configs \
    \- *backup_with_cli_backup.yml*: Backup IOS and EOS using the generic `ansible.netcommon.cli_backup` module \
    \- *backup_with_napalm.yml*: Backup IOS, EOS and NXOS using napalm (not sure if ASAs or F5 still work)

3. create_vlan \
    \- *playbook_create_vlans.yml*: Build and verify VLANs on IOS

4. network_state_report \
    \- *playbook_main.yml*: Generates tables of device state (asa, nxos, ios, bigip) for network elements (Interfaces, MACs, ARPs, VPN, OSPF, BGP) and builds a report
