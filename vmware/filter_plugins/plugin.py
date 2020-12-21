import os

class FilterModule(object):
    def filters(self):
        return {
            'nested_3layer': self.nest_3l
        }

    def nest_3l(self, vm_tmpl):
        all_sites = []
        for site in vm_tmpl:
            all_vms = []
            os_type = site.pop('type')
            for each_type in os_type:
                for each_vm in each_type['vms']:
                    each_vm['tmpl'] = each_type['tmpl']
                    each_vm['timezone'] = each_type.get('timezone')
                    each_vm['state'] = each_vm.get('state', each_type.get('state', 'poweredon'))
                    # Depends whether location to build the VM is set or not
                    if each_vm.get('dir') != None:
                        each_vm['dir'] = os.path.join(site['base_dir'], each_vm['dir'])
                    else:
                        each_vm['dir'] = site['base_dir']
                    all_vms.append(each_vm)
            site['vms'] = all_vms
            all_sites.append(site)
        return all_sites