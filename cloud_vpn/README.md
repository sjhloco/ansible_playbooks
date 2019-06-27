# Create Site-to-site VPN to Azure

Creates a route-based VPN between a small office/home and Azure.
The playbook is designed to be run from an Ansible host behind the ASA as it automatically grabs the local IP address to use in the creation of the VPN. This can be manually overridden by editing the variable *rm_public_ip*.
Tested from Azure to an ASA 5505 running 9.2(4). 

Azure is missing Ansible modules for creating the *Local Network Gateway* and *VPN Connection* so the playbook uses *AZ CLI* for these tasks. It utomatically logs in and out of *AZ CLI* when performing these tasks using the credentials from the Azure Ansible modules (credentials file).

### Prerequisites ###
1. Install AZ CLI on the Ansible host.
<br/>*Redhat: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-apt?view=azure-cli-latest*
<br/>*Azure: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-yum?view=azure-cli-latest*
2. Create the Service Principal Credentials that are used for authentication by the Azure modules.
<br/>*az ad sp create-for-rbac --name Ansible				                   Created APP_ID called Ansible*
<br/>*az login --service-principal --username APP_ID --password PASSWORD --tenant TENANT_ID		   To test*
3. Get the Azure SubscriptionID (the 2nd dictionary key *id*).
<br/>*az account show*
4. In the home directory of the Ansible host create an Azure directory and credentials file with the following details.
<br/>*mkdir ~/.azure*
<br/>*vi ~/.azure/credentials*
<br/>*[default]*
<br/>*subscription_id=<your-subscription_id>*
<br/>*client_id=<security-principal-appid>*
<br/>*secret=<security-principal-password>*
<br/>*tenant=<security-principal-tenant>*
5. Remove a conflicting Python cryptography package and install the required Ansible Azure packages.
<br/>*sudo pip uninstall -y cryptography*
<br/>*pip install ansible[azure] --user*

### Running the playbook ###
The playbook can be run with the following tags:

**--tag deploy:** Assumes that nothing is created. If not already existing it will createthe following.
<br/>AZ: *Resource_group, Public_ip, virtual_network, subnets, gateway_subnets, VPN_gateway, local_network_gateway, vpn_connection (and ipsec_policy)*
<br/>ASA: *ikev2_policy, ikev2_ipsec_proposal, crypto_map, interesting_traffic_ACL, outside_acl, nonat, tunnel-group*

**--tag destroy:** Only removes the configuration specific to to this VPN tunnel, so wont remove any of the AZ vnet/subnets or the ASA ikev2_policy/ipsec_proposal.
<br/>AZ: *Public_ip, local_network_gateway, VPN_gateway, vpn_connection (and ipsec_policy)*
<br/>AZ: *Crypto_map_100, ACLs, object-groups, nonat, tunnel-group*
 
**--tag vpn_down:**	Deletes the components to break the VPN (more importantly the elements that Azure bills you for).
<br/>AZ: *VPN_gateway, vpn_connection (including ipsec_policy)*
<br/>ASA: *Crypto_map_100 set peer, tunnel-group*

**--tag vpn_up:** Brings backup the tunnel by adding back the components deleted by vpn_down and updating the local gateway incase the remote peer address had changed.
<br/>AZ: *VPN_gateway, vpn_connection (including ipsec_policy)*
<br/>ASA: *Crypto_map_100 set peer tunnel-group*

The interesting traffic and pre-shared key can be updated by re-running *deploy*. The crypto algorithmns (*vpn-connection ipsec policy*) can not be updated, to change these the vpn connection must be deleted (*vpn_down*) and added back (*vpn_up*). This is a limitation of Azure itself rather than the playbook.
