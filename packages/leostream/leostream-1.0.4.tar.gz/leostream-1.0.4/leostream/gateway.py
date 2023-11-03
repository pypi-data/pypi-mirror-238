from .restapi import LeostreamClient
from .webresource import WebResource

class LeostreamGateway(WebResource):
    
    resource_type = "gateways"

    def __init__(self,id=None, name=None, address=None) -> None:
        ''' Goal: Create a gateway with the name and address passed to the function OR get the existing gateway data for the id passed to the function.
            Steps:
            1. Get a reference to the Leostream API
            2. If the id is None, create a new gatweway via the API
            3. If the id is not None, get the gateway data via the API'''
        self._api = LeostreamClient()   
        if id is None:
            self._URL="https://"+str(self._api.broker)+"/rest/v1/gateways/"
            # create an emtpy json object to store the data
            self.data = {
                    "address": address,
                    "name": name,
            }
            self.data = self.create()
            self._id = self.data['id']
        else:
            self._id = id
            self._URL="https://"+str(self._api.broker)+"/rest/v1/gateways/"+ str(self._id)
            self.data = self.get()
