class FilterModule(object):			
    def filters(self):			
        return {		
            'az_login': self.az_login  
        }
    def az_login(self, az_creds): 
        temp_list =[]
        temp_dict = {}
        for x in az_creds.splitlines()[1:]:
            temp_list = x.split('=')    # Creates list by splitting at =
            temp_dict[(temp_list[0])] = temp_list[1]    # creates a dict of list elements from each line
        return "az login --service-principal -u {} -p {} --tenant {}".format(temp_dict['client_id'], temp_dict['secret'], temp_dict['tenant'])
