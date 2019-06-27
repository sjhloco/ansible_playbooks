class FilterModule(object):			
    def filters(self):			
        return {		
            'delete_vpn': self.delete_vpn        
        }
 
    def delete_vpn(self, raw_config, vpn_interface, cl_provider, vpn_index, crypto_map, cl_public_ip, pfs, p2_encr, sa_life, sa_size):
        del_config = None
        for y in raw_config[0].splitlines():
        # Deletes nat statement and outside ACL    
            if "access-list {}".format(vpn_interface) in y:
                del_config = "no access-list {} extended permit ip object-group {}_REMOTE object-group {}_LOCAL".format(vpn_interface, cl_provider.upper(), cl_provider.upper())
            if "nat (any,{}".format(vpn_interface) in y:
                del_config += "\nno nat (any,{}) source static {}_LOCAL {}_LOCAL destination static {}_REMOTE {}_REMOTE".format(vpn_interface, 
                                                                                                                                cl_provider.upper(), 
                                                                                                                                cl_provider.upper(), 
                                                                                                                                cl_provider.upper(), 
                                                                                                                                cl_provider.upper())
        # Deletes transmit map vpn_index
            if "{} match address".format(vpn_index) in y:
                del_config += "\nno crypto map {} {} match address {}_VPN".format(crypto_map, vpn_index, cl_provider.upper())
            if "{} set peer".format(vpn_index) in y:
                del_config += "\nno crypto map {} {} set peer {}".format(crypto_map, vpn_index,cl_public_ip)
            if "{} set pfs".format(vpn_index) in y:
                del_config += "\nno crypto map {} {} set pfs group{}".format(crypto_map, vpn_index, pfs)
            if "{} set ikev2".format(vpn_index) in y:
                del_config += "\nno crypto map {} {} set ikev2 ipsec-proposal AES-{}".format(crypto_map, vpn_index, p2_encr)
            if "{} set security-association lifetime sec".format(vpn_index) in y:                                             
                del_config += "\nno crypto map {} {} set security-association lifetime seconds {}".format(crypto_map, vpn_index, sa_life)
            if "{} set security-association lifetime kilo".format(vpn_index) in y:                                             
                del_config += "\nno crypto map {} {} set security-association lifetime kilobytes {}".format(crypto_map, vpn_index, sa_size)                    
        # Deletes tunnel-group cl_public_ip          
            if "tunnel-group {}".format(cl_public_ip) in y:
                del_config += "\nclear configure tunnel-group {}".format(cl_public_ip)
    # Deletes VPN ACL and object groups, need to rerun loop as at start of running config
        for y in raw_config[0].splitlines():
            if "access-list {}_VPN".format(cl_provider.upper()) in y:    
                del_config += "\nclear configure access-list {}_VPN".format(cl_provider.upper())
        for y in raw_config[0].splitlines():            
            if "object-group network {}_LOCAL".format(cl_provider.upper()) in y:
                del_config += "\nno object-group network {}_LOCAL".format(cl_provider.upper())
            if "object-group network {}_REMOTE".format(cl_provider.upper()) in y:    
                del_config += "\nno object-group network {}_REMOTE".format(cl_provider.upper())
    # Only returns avalue if the variable del_config has any content           
        if del_config != None:
            return del_config


    