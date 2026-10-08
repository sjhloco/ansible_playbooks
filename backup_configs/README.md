# Backup Configurations

Text-based running configs backups using `ansible.netcommon.cli_backup`, seems a better option than OS type backups, Napalm backups still work, but these days doesnt really seem developed/supported and `ansible_network_os` must be shorthand (not FQDN).

Tested on NXOS, IOS and EOS (ASA and F5s not tested on newer Ansible releases)

The order of operation is:
1. Create new temp directory
2. Clone a GIT repo to this directory
3. Backup running config of all nxos, ios and asa devices in the inventory and copy to the temp directory
4. Create a F5 UCS and copy to the temp directory
5. Commit and push the changes back to the git repo
6. Delete the temp directory
