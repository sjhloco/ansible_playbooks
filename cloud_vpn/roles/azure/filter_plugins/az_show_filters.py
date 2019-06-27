class FilterModule(object):			
    def filters(self):			
        return {		
            'list_rm_prfxs': self.list_rm_prfxs,	 
            'rm_prfxs': self.rm_prfxs,               				
            'check_az_show': self.check_az_show          
        }
 # Convert the dict of remote subnets into a list     
    def list_rm_prfxs(self, rm_subnets):			
        prfxs = []
        for x in rm_subnets.values():
            prfxs.append(x)
        return prfxs
 # Flattern the list of remote subnets so can be used in the az cmd       
    def rm_prfxs(self, rm_subnets):			
        prfxs = []
        for x in rm_subnets.values():
            prfxs.append(x)
        return ' '.join(prfxs)

 # Check for whether vpn_conn is in the list of actvie ones got from azure     
    def check_az_show(self, az_show, obj_name):	
        if obj_name in az_show:
            return True
        else:
            return False