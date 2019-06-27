# Create Site-to-site VPN to Azure

Creates a route-based VPN between a small office/home and Azure.
The playbook is designed to be run from an Ansible host behind the remote device as it automatically grabs the local IP address to use in the creation of the VPN. This can be manually overridden by editing the variable rm_public_ip.
Tested from Azure to an ASA 5505 running 9.2(4). 

Azure is missing Ansible modules for creating the *Local Network Gateway* and *VPN Connection* so the playbook uses AZ CLI for these tasks. It will automatically log in and out of AZ CLI when performing these specific tasks using the credentials from the Azure Ansible modules (credentials file).

### Prerequisites: ###
1. Install AZ CLI on the Ansible host
*Redhat: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-apt?view=azure-cli-latest		
Azure: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-yum?view=azure-cli-latest*
2. Create the Service Principal Credentials that are used for authenticate by the Azure modules
*az ad sp create-for-rbac --name Ansible				Created APP_ID called Ansible
az login --service-principal --username APP_ID --password PASSWORD --tenant TENANT_ID		To test*
3. Get Azure SubscriptionID, is the 2nd dictionary with a value of *id*
*az account show*
4. In the home directory of the Ansible host create an azure directory andcredentials file and add the the credential details to it
*mkdir ~/.azure
vi ~/.azure/credentials
[default]
subscription_id=<your-subscription_id>
client_id=<security-principal-appid>
secret=<security-principal-password>
tenant=<security-principal-tenant>*
5.Remove conflicting Python cryptography package and install the required Ansible Azure packages
*sudo pip uninstall -y cryptography
pip install ansible[azure] --user*

### Running the playbook ###
The playbook can be run with the following tags:

**--tag deploy:** Assumes that nothing is already created. If it does not already creates the following:
*AZ: Resource_group, Public_ip, virtual_network, subnets, gateway_subnets, VPN_gateway, local_network_gateway, vpn_connection (and ipsec_policy)*
*ASA: ikev2_policy, ikev2_ipsec_proposal, crypto_map, interesting_traffic_ACL, outside_acl, nonat, tunnel-group*

**--tag destroy:** Only removes the config specific to to this VPN connection, so wont remove any of the AZ vnet/subnets or the ASA ikev2_policy/ikev2_ipsec_proposal
*AZ: Public_ip, local_network_gateway, VPN_gateway, vpn_connection (and ipsec_policy)
AZ: Crypto_map_100, ACLs, object-groups, nonat, tunnel-group*
 
**--tag vpn_down:**	Just takes down the elements to break the VPN (and more importantly the elements that Azure bills you for)
*AZ: VPN_gateway, vpn_connection, (including vpn_connection_ipsec_policy)
ASA: Crypto_map_100 set peer adn tunnel group*

**--tag vpn_up:** Brings backup the tunnel by adding back the cmds deleted by vpn_down and updating the local gateway (incase peer addres had changed)
*AZ: VPN_gateway, vpn_connection, (including vpn_connection_ipsec_policy)
ASA: Crypto_map_100 set peer adn tunnel group*

The interesting traffic and pre-shared key can be updated by re-running deploy. The crypto algorithmns (vpn-connection ipsec policy) can not be updated, to change these the vpn connection must be deleted (vpn_down) and added back (vpn_up). This is a limitation of Azure itself rather than the playbook.
