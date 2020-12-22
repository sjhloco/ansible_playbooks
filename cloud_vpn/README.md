# Create Site-to-site VPN - ASA to Azure

Creates a route-based VPN with policy-based traffic selectors (crypto-map not VTI) between a Cisco ASA and Azure.\
The playbook is designed to be run from an Ansible host behind the ASA as it automatically grabs the local IP address to use in the creation of the VPN. This can be manually overridden by editing the variable *rm_public_ip*.\
The interesting traffic for the VPN is the Azure Virtual Network with the subnest within that filtered on the ASA Outside ACL.\
Azure is missing Ansible modules for creating the *Local Network Gateway* and *VPN Connection* so the playbook uses *AZ CLI* for these tasks.

The ASA credentials are defined under the **asa.yml** group_var and the Azure credentials in the **~/.azure/credentials** file (as described in Prerequisites)

### Versions
ASA: Tested on ASA5505 running 9.2(4) and ASA5506 running 9.8(4)22\
Ansible: 2.8.4\
Python: 3.6.9

### Prerequisites
1. Install AZ CLI on the Ansible host\
*Ubuntu: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-apt?view=azure-cli-latest* \
*RedHat: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-yum?view=azure-cli-latest*

2. Create a Service Principal Credential Azure module authentication (2nd command tests it)
```css
az ad sp create-for-rbac --name Ansible
az login --service-principal --username APP_ID --password PASSWORD --tenant TENANT_ID
```

3. Get the Azure SubscriptionID (the 2nd dictionary key *id*)
```css
az account show
```

4. In the home directory of the Ansible host create an Azure directory and credentials file with the following details:
```css
mkdir ~/.azure
vi ~/.azure/credentials
[default]
subscription_id=your-subscription_id
client_id=security-principal-appid
secret=security-principal-password
tenant=security-principal-tenant
```

5. Remove the conflicting Python cryptography package and install the Ansible Azure packages
```css
sudo pip uninstall -y cryptography
pip install ansible[azure] --user
```

### Variables
The varibles that are used in the playbook are split between three files:

**asa.yml:** ASA specific variables
- *ansible_user:* ASA username
- *ansible_ssh_pass:* ASA password
- *vpn_index:* Index number used for the phase1 ikev2 policy and the crypto-map
- *crypto_map:* Name of the crypto-map
- *vpn_interface:* The interface that the ikev2 policy and crypto-map are associated to and what is used in the NoNAT statement
- *outside_acl:* Name of the ingress ACL used to limit access from the individual subnets (*no sysopt connection permit-vpn*)
- *asa_vpn.acl:* Name of the VPN interesting traffic ACL
- *asa_vpn.local_grp:* Name of the object-group that holds the networks local to the ASA
- *asa_vpn.az_vnet_grp:* Name of the object-group that holds the remote cloud Virtual Networks (supernets)
- *asa_vpn.az_subnet_grp:* Name of the object-group that holds the remote cloud Virtual Network subnets

**azure.yml:** Azure specific variables
- *cld_region:*  Azure region in which to build all the VPN objects
- *rg_name:* Azure resource-group name
- *public_ip_name:* Name of the Azure public IP address object
- *vn_name:* The Azure virtual-network name that holds the address spaces allowed over the VPN (interesting traffic)
- *gw_subnet_name:* Azure gateway subnet name. It is the equivalent of a P-t-P link between VPN gateway and the Virtual Network
- *gw_subnet_prfx:* Azure gateway subnet network/prefix
- *cld_gateway:* Azure virtual network gateway name. The GW binds all the Azure VPN elements together (VNET and public IP)
- *rmte_gateway:* Name of Azure object used to group the remote site peer (public) IP address and subnets (interesting traffic)
- *vpn_connection:* The Azure VPN connection links the Azure virtual network gateway and remote public IP and subnets

**all.yml:** VPN variables such as interesting traffic, PSK, encryption and hashing algorithms
- *cld_provider:* Cloud provider name that is used in the ASA object names
- *rmte_location:* VPN remote site name that is used in the Azure object names
- *rmte_public_ip:* Public IP address of the remote site (ASA). By default this is hashed out and gathered automatically
- *rmte_subnets:* Subnets of the networks at the remote site (behind the ASA)
- *cld_public_ip:* Public IP address of the cloud provider (Azure). By default this is hashed out and gathered automatically
- *vn_addr_spc:* List of address spaces (supernets) within the virtual network (Azure). This is used as the interesting traffic on the ASA
- *cl_subnets:* Dictionary of the subnets within the Azure Virtual Network. These are filtered through the ASA Outside ACL
- *p1_encr:* Phase1 encryption algorithm
- *p1_hash* Phase1 hashing (integrity) algorithm
- *dh:* Phase1 Diffie-Hellman (DH) Group
- *p1_life:* Phase1 SA lifetime (only applied on ASA)
- *p2_encr:* Phase2 encryption algorithm
- *p2_hash:* Phase2 hashing (integrity) algorithm
- *pfs:* Phase2 Perfect Forward Secrecy (PFS) group
- *sa_life:* Phase2 SA lifetime in seconds
- *sa_size:* Phase2 SA lifetime in KiloBytes
- *psk:* Pre-shared Key

### Running the playbook ###
The playbook can be run with any of the following tags:

**--tag deploy:** Assumes that nothing is created. If not already existing it will create the following.\
AZ: *resource_group, public_ip, virtual_network, subnets, gateway_subnets, VPN_gateway, local_network_gateway, vpn_connection, ipsec_policy*\
ASA: *ikev2_policy, ikev2_ipsec_proposal, crypto_map, interesting_traffic_ACL, outside_acl, nonat, tunnel_group*

**--tag destroy:** Only removes the configuration specific to to this VPN tunnel, so wont remove any of the AZ vnet/subnets or the ASA ikev2_policy/ipsec_proposal.\
AZ: *public_ip, local_network_gateway, VPN_gateway, vpn_connection, ipsec_policy)*\
ASA: *crypto_map, ACLs, object_groups, nonat, tunnel_group*

**--tag vpn_down:**	Deletes the components to break the VPN (more importantly the elements that Azure bills you for).\
AZ: *VPN_gateway, vpn_connection, ipsec_policy*\
ASA: *crypto_map set peer, tunnel-group*

**--tag vpn_up:** Brings backup the tunnel by adding back the components deleted by vpn_down and updating the local gateway incase the remote peer address has changed.\
AZ: *VPN_gateway, vpn_connection, ipsec_policy*\
ASA: *crypto_map set peer, tunnel_group*

The interesting traffic and pre-shared key can be updated by re-running *deploy*.\
The crypto algorithmns (*vpn-connection ipsec policy*) cannot be updated, to change these the vpn connection must be deleted (*vpn_down*) and added back (*vpn_up*).\
Everytime *deploy* or *vpn_up* the ASA tunnel-group will show that it has been changed as the PSK is hashed on the ASA so Ansible will always think it has changed
