class FilterModule(object):
    def filters(self):
        return {
            'delete_vpn': self.delete_vpn
        }

    def delete_vpn(self, raw_config, vpn_interface, outside_acl, vpn_index, crypto_map, cld_public_ip, asa_vpn, pfs, p2_encr, sa_life, sa_size):

        del_config = ""
        for y in raw_config[0].splitlines():
        # Deletes nat statement and outside ACL
            if "access-list {}".format(outside_acl) in y:
                del_config += "no access-list {} extended permit ip object-group {} object-group {}".format(outside_acl, asa_vpn['az_subnet_grp'], asa_vpn['local_grp'])
            if "nat (any,{}".format(vpn_interface) in y:
                del_config += "\nno nat (any,{0}) source static {1} {1} destination static {2} {2}".format(vpn_interface, asa_vpn['local_grp'], asa_vpn['az_vnet_grp'])

        # Deletes transmit map vpn_index
            if "{} match address".format(vpn_index) in y:
                del_config += "\nno crypto map {} {} match address {}".format(crypto_map, vpn_index, asa_vpn['acl'])
            if "{} set peer".format(vpn_index) in y:
                del_config += "\nno crypto map {} {} set peer {}".format(crypto_map, vpn_index,cld_public_ip)
            if "{} set pfs".format(vpn_index) in y:
                del_config += "\nno crypto map {} {} set pfs group{}".format(crypto_map, vpn_index, pfs)
            if "{} set ikev2".format(vpn_index) in y:
                del_config += "\nno crypto map {} {} set ikev2 ipsec-proposal AES-{}".format(crypto_map, vpn_index, p2_encr)
            if "{} set security-association lifetime sec".format(vpn_index) in y:
                del_config += "\nno crypto map {} {} set security-association lifetime seconds {}".format(crypto_map, vpn_index, sa_life)
            if "{} set security-association lifetime kilo".format(vpn_index) in y:
                del_config += "\nno crypto map {} {} set security-association lifetime kilobytes {}".format(crypto_map, vpn_index, sa_size)

        # Deletes tunnel-group cld_public_ip and VPN_ACL
            if "tunnel-group {}".format(cld_public_ip) in y:
                del_config += "\nclear configure tunnel-group {}".format(cld_public_ip)
            if "access-list {}".format(asa_vpn['acl']) in y:
                del_config += "\nclear configure access-list {}".format(asa_vpn['acl'])

        # Deletes the object groups, need to rerun loop as at start of running config
        for y in raw_config[0].splitlines():
            if "object-group network {}".format(asa_vpn['local_grp']) in y:
                del_config += "\nno object-group network {}".format(asa_vpn['local_grp'])
            if "object-group network {}".format(asa_vpn['az_vnet_grp']) in y:
                del_config += "\nno object-group network {}".format(asa_vpn['az_vnet_grp'])
            if "object-group network {}".format(asa_vpn['az_subnet_grp']) in y:
                del_config += "\nno object-group network {}".format(asa_vpn['az_subnet_grp'])

    # Only returns avalue if the variable del_config has any content
        if del_config != "":
            return del_config


