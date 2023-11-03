from .restapi import LeostreamClient
from .webresource import WebResource

class LeostreamCenter(WebResource):
    
    resource_type = "centers"

    def __init__(self,id) -> None:
        self._api = LeostreamClient()
        self._id = id
        self._URL="https://"+str(self._api.broker)+"/rest/v1/centers/"+ str(self._id)
        self.data = self.get()

    def retrieve_image_name(self, image_id):
        ''' Goal: Retrieve the image name for the image id passed to the function.
            Steps:
            1. Get the image name for the image id passed to the function from the center
            2. Return the image name '''
        
        # Get the he current image name by id       
        ami = [x for x in self.data['images'] if x["id"]==image_id]
        return ami[0]['name']
