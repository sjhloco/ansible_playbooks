class FilterModule(object):			
    def filters(self):			
        return {		
            'num_vlans': self.num_vlans,        
            'dev_vlans': self.dev_vlans            
        }
 # Convert the dict of remote subnets into a list     
    def num_vlans(self, device_vlans):			
        num_vlans = []
        for x in device_vlans:
            num_vlans.append(x["VLAN_ID"])
        return len(num_vlans)    
    
    def dev_vlans(self, device_vlans):			
        dev_vlans = {}
        for x in device_vlans:
            dev_vlans[x["VLAN_ID"]] = x['NAME']
        return dev_vlans
