# Backup Configurations

Originally created using Ansible networking command modules (backup_with_cmd_mod.yml) but edited to use NAPALM as a lot more scalable (backup_with_napalm.yml).
Should use NAPALM playbook, original one only kept for reference.

Tested on NXOS, IOS, ASA and F5s.

The order of operation is:
1. Create new temp directory
2. Clone a GIT repo to this directory
3. Backup running config of all nxos, ios and asa devices in the inventory and copy to the temp directory
4. Create a F5 UCS and copy to the temp directory
5. Commit and push the changes back to the git repo
6. Delete the temp directory
