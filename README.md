# Ansible Playbooks

Contains all playbooks created for small tasks

1. collect-data<br />
-collect_in_one_file.yml: Runs cmds and stores output in one separate file (using templates)<br />
-collect_in_separate_files.yml: Runs cmds and stores output of commands in separate files<br />

2. backup_configs<br />
-backup_with_cmd_mod.yml: Backs up ASAs, IOS and NXOS using Ansible command modules in seperate plays <br />
-backup_with_napalm.yml: Backs up ASAs, IOS and NXOS using napalm and F5 using bigip module l<br />
