# Creates VLANs and validates that they have been added

These first 2 tasks have `check_mode: false`, this means they "always run this task for real, even when the playbook runs with -C".
1. Create a new fresh file structure (clears any files from previous playbook runs), don't report changes to Ansible.
2. Gets current device VLANs and passes these through custom filters (python) to get count of VLANs and a dict of all non-default VLANs ({id: name})

3. Declaratively creates the new VLANs using Resource module, `ansible.netcommon.network_resource` abstracts OS in the one play
    - `check_mode: false` just prints the commands to be run
    - When changes are made prints the before/after config difference

4. Post-checks will only run if a change is made, so result variable has changed
    - Gathers the device VLANs and passes results through filter plugin
    - Validates that the number of VLANs on the device matches what is expected
    - Validates the naming and number of VLANs on device matches input data
