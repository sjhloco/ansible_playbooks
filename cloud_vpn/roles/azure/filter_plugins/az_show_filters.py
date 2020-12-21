class FilterModule(object):
    def filters(self):
        return {
            'rmte_prfxs': self.rmte_prfxs,
            'check_az_show': self.check_az_show
        }
 # Flattern the list of remote subnets so can be used in the az cmd
    def rmte_prfxs(self, rmte_subnets):
        prfxs = []
        for x in rmte_subnets:
            prfxs.append(x)
        return ' '.join(prfxs)

 # Check for whether vpn_conn is in the list of active ones got from azure
    def check_az_show(self, az_show, obj_name):
        if obj_name in az_show:
            return True
        else:
            return False