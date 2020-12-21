# Create Site-to-site VPN - ASA to Azure

Creates a route-based VPN with policy-based traffic selectors (crypto-map not VTI) between a Cisco ASA and Azure.\
The playbook is designed to be run from an Ansible host behind the ASA as it automatically grabs the local IP address to use in the creation of the VPN. This can be manually overridden by editing the variable *rm_public_ip*.\
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
- *vpn_interface:* Interface used in the NoNAT statement aswell as what ikev2 policy and crypto-map are associated to
- *outside_acl:* Name of the Outside ACL which is used for limiting access from the indivudal subnets (*no sysopt connection permit-vpn*)
- *asa_vpn.acl:* Name of the VPN ACL
- *asa_vpn.local_grp:* Name of the object-group that holds the networks local to the ASA
- *asa_vpn.az_vnet_grp:* Name of the object-group that holds the Virtual Networks (supernets)
- *asa_vpn.az_subnet_grp:* Name of the object-group holds the Virtual Network subnets

**azure.yml:** Azure specific variables
-*cl_region:*  Azure region in which to build VPN objects
-*rg_name:* Azure resource-group name

*public_ip_name:* Name of the Azure public IP object. An ansible fact is automaticall created for this
*vn_name:* Azure virtual-network name that holds the address spaces allowed over the VPN
*gw_subnet_name:* Azure Gateway subnet name, like p-t-p link) between VPN gateway and the Virtual Network
*gw_subnet_prfx:* Azure Gateway subnet network/prefix, like p-t-p link) between VPN gateway and the Virtual Network

*cl_gateway:* Azure virtual network gateway name, binds all the Azurw VPN elements together (VNET, public IP)
*rm_gateway:* Name of Azure object to group remote site publicIP and subnets (interesting traffic)
*vpn_connection:* Azures VPN connection links Azure virtual network gateway and remote public IP and networks

**all.yml:** VPN variables such as interesting traffic, PSK, encryption and hashing algorithms
*cl_provider:* Cloud provider name used in ASA object names
*rm_location:* VPN remote end used to create cloud provider object names

Remote-side VPN variables - Interesting traffic and public IP address
*rm_public_ip:* Public IP address of the remote site (ASA). By default this is hashed out and got automatically
*rm_subnets:* Subnets of the networks at the remote site *behind (ASA)

Cloud-side VPN variables - Interesting traffic and peer
*vn_addr_spc* List of address spaces (supernets) within the virtual network. Are used as the interesting traffic on the ASA
*cl_subnets:* Dictionary {name: network/prefix } of the subnest within the Azure Virtual Network. Are allowed in the Outside ACL on the ASA

VPN encryption (AES), hashing (SHA) algorithms and PSK
*p1_encr*
*p1_hash*
*dh*
*p1_life*
*p2_encr*
*p2_hash*
*pfs*
*sa_life*
*sa_size*
*psk*

### Running the playbook ###
The playbook can be run with the following tags:

**--tag deploy:** Assumes that nothing is created. If not already existing it will createthe following.\
AZ: *Resource_group, Public_ip, virtual_network, subnets, gateway_subnets, VPN_gateway, local_network_gateway, vpn_connection (and ipsec_policy)*\
ASA: *ikev2_policy, ikev2_ipsec_proposal, crypto_map, interesting_traffic_ACL, outside_acl, nonat, tunnel-group*

**--tag destroy:** Only removes the configuration specific to to this VPN tunnel, so wont remove any of the AZ vnet/subnets or the ASA ikev2_policy/ipsec_proposal.\
AZ: *Public_ip, local_network_gateway, VPN_gateway, vpn_connection (and ipsec_policy)*\
ASA: *Crypto_map_100, ACLs, object-groups, nonat, tunnel-group*

**--tag vpn_down:**	Deletes the components to break the VPN (more importantly the elements that Azure bills you for).\
AZ: *VPN_gateway, vpn_connection (including ipsec_policy)*\
ASA: *Crypto_map_100 set peer, tunnel-group*

**--tag vpn_up:** Brings backup the tunnel by adding back the components deleted by vpn_down and updating the local gateway incase the remote peer address had changed.\
AZ: *VPN_gateway, vpn_connection (including ipsec_policy)*\
ASA: *Crypto_map_100 set peer tunnel-group*

The interesting traffic and pre-shared key can be updated by re-running *deploy*.\
The crypto algorithmns (*vpn-connection ipsec policy*) cannot be updated, to change these the vpn connection must be deleted (*vpn_down*) and added back (*vpn_up*).
