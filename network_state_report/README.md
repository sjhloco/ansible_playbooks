# Network/Device State Report

This playbook collects information from devices creating a results table for each network element before combining these into an overall report. Each network element is a separate `role` that creates a table for that element. `tags` can be used to only run individual elements or combine a subset of elements.

The tables created for each element are stored in a temporary folder (`~/network_state/tmp_tables`) that is deleted at the start of each playbook run. The report assembles all these tables into the one file (`~/network_state/network_state_YYYY-MM-DD_HHMM.txt`), this not deleted at the start of each playbook run.

The command outputs are passed through python filters along with expected network state (from `group_vars`) to create a list of each devices results that are eventually used by the `reports` python filter to build the tables. The following device or role specific `group_vars` are used to define the desired state.

| group_var | variables |
| --------- | --------- |
| `asa.yml` | `ospf_neigh`, `vpn_peer` |
| `iosxe.yml` | `ospf_neigh`, `bgp_neigh`, `vpn_peer` |
| `spine.yml`, `leaf.yml`, `border_leaf.yml` | `bgp_neigh`, `ospf_neigh` |

## Tags and Tables

| --tag | Table headers | File |
| ----- | ------------- | ---- |
| `bgp` | Expected BGP Peers, Enabled BGP Peers, UP BGP Peers, Received prefixes | /tmp/network_state/tmp_tables/bgp_table.txt |
| `edge` | Total L2L VPNs, Up L2L VPNs, Total NAT Translations | /tmp/network_state/tmp_tables/edge_table.txt |
| `intf` | VLANs',&nbsp; 'MACs, Configured POs, UP POs, PO member ports, UP PO member ports | /tmp/network_state/tmp_tables /interface_table.txt |
| `l2` | ARP Table, Routing Table | /tmp/network_state/tmp_tables/l2_table.txt |
| `l3` | Enabled Interfaces, UP Interfaces, LLDP Neighbors | /tmp/network_state/tmp_tables/l3_table.txt |
| `ospf` | Expected Neighors, UP Neighbors, Total LSAs | /tmp/network_state/tmp_tables/ospf_table.txt |
| `vip` | Enabled VIPs, UP VIPs, Total Nodes, UP Nodes | /tmp/network_state/tmp_tables/vip_table.txt |
| `report` | Builds main directory, cleans the tmp directory and assembles all the tables | /tmp/network_state/network_state_DATE/txt |

## Network Modules

When I originally built this not all modules could collect and parse all the desired outputs so the playbook uses a combination of `napalm_get_facts`, `bigip_device_info` as well as Ansible modules `cli_command` and `cli_parse` (with pyats). These days there is probably a more vendor-agnostic way to do this using the same module. The `username` and `password` for all devices (except F5s) are stored in `group_vars/all.yml`.

### Tested

I recently rewrote the playbook for Ansible 2.21 but didn`t have NXOS, ASA or F5 available to test on. In theory these should still work but be warned there maybe the odd teething problem with them. It was originally tested on the following versions of virtual equipment:
- F5: 13.1.1
- N9K: 7.0(3)I7(6)
- ASAv: 9.9(1)
- CSR: 16.06.02
- vIOS: 15.2

### Example Report

===== BGP Table =====

|      Device     | Expected Peers | Enabled Peers | UP Peers | pfxrcd |
| --------------- | -------------- | ------------- | -------- | ------ |
|  dc1-n9k-spine1 |       3        |       3       |    3     |   26   |
|  dc1-n9k-spine2 |       3        |       3       |    3     |   26   |
|  dc1-n9k-leaf1  |       2        |       2       |    2     |   12   |
|  dc1-n9k-leaf2  |       2        |       2       |    2     |   12   |
| dc1-n9k-border1 |       4        |       4       |    4     |   44   |
|  dc1-csr-xnet1  |       4        |       4       |    4     |   4    |

===== Edge Table =====

|     Device    | Total L2L VPNs | Up L2L VPNs | Total NAT Translations |
| ------------- | -------------- | ----------- | ---------------------- |
| dc1-csr-xnet1 |       0        |      0      |           1            |
| dc1-asav-xfw1 |       0        |      0      |           3            |

===== Interface Table =====

|      Device     | Enabled Interfaces | UP Interfaces | LLDP Neighbors |
| --------------- | ------------------ | ------------- | -------------- |
|  dc1-n9k-spine1 |         9          |       9       |       3        |
|  dc1-n9k-spine2 |         9          |       9       |       3        |
|  dc1-n9k-leaf1  |         22         |       22      |       5        |
|  dc1-n9k-leaf2  |         22         |       22      |       5        |
| dc1-n9k-border1 |         10         |       10      |       3        |
|   dc1-vios-sw1  |         6          |       6       |       0        |
|  dc1-csr-xnet1  |         6          |       6       |       1        |
|  dc1-asav-xfw1  |         4          |       8       |       0        |

===== Layer2 Table =====

|     Device    | VLANs | MACs | cfg POs | UP POs | PO member ports | UP PO member ports |
| ------------- | ----- | ---- | ------- | ------ | --------------- | ------------------ |
|  dc1-vios-sw1 |   11  |  3   |    1    |   1    |        2        |         2          |
| dc1-n9k-leaf1 |   9   |  14  |    4    |   4    |        4        |         4          |
| dc1-n9k-leaf2 |   9   |  14  |    4    |   4    |        4        |         4          |

===== Layer3 Table =====

|      Device     | ARP Table | Routing Table |
| --------------- | --------- | ------------- |
|  dc1-csr-xnet1  |     11    |       18      |
|  dc1-asav-xfw1  |     4     |       20      |
|  dc1-n9k-spine1 |     5     |       10      |
|  dc1-n9k-spine2 |     5     |       10      |
|  dc1-n9k-leaf1  |     8     |       25      |
|  dc1-n9k-leaf2  |     8     |       25      |
| dc1-n9k-border1 |     6     |       25      |

===== OSPF Table =====

|      Device     | Expected Neighors | UP Neighbors | Total LSAs |
| --------------- | ----------------- | ------------ | ---------- |
|  dc1-csr-xnet1  |         1         |      1       |     4      |
|  dc1-asav-xfw1  |         2         |      2       |     12     |
|  dc1-n9k-spine1 |         3         |      3       |     5      |
|  dc1-n9k-spine2 |         3         |      3       |     5      |
|  dc1-n9k-leaf1  |         3         |      3       |     5      |
|  dc1-n9k-leaf2  |         3         |      3       |     5      |
| dc1-n9k-border1 |         3         |      3       |     13     |

===== VIP Table =====

|    Device   | Enabled VIPs | UP VIPs | Total Nodes | UP Nodes |
| ----------- | ------------ | ------- | ----------- | -------- |
| dc1-ltm-lb1 |      2       |    1    |      3      |    2     |
