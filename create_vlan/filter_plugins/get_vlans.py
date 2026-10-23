class FilterModule(object):  # noqa: UP004
    def filters(self):
        return {"num_vlans": self.num_vlans, "device_vlans": self.device_vlans}

    # Convert the dict of remote subnets into a list
    def num_vlans(self, device_vlans):
        num_vlans = []
        for x in device_vlans:
            if "default" not in x["name"]:
                num_vlans.append(x["vlan_id"])
        return len(num_vlans)

    def device_vlans(self, device_vlans):
        vlan_dict = {}
        for x in device_vlans:
            if "default" not in x["name"]:
                vlan_dict[x["vlan_id"]] = x["name"]
        return vlan_dict
