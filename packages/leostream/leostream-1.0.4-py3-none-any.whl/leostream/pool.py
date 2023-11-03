from .restapi import LeostreamClient
from .webresource import WebResource
from .center import LeostreamCenter

class LeostreamPool(WebResource):
    
    resource_type = "pools"

    def __init__(self, id=None, name=None, center_id=None) -> None:
        ''' Goal: Create a new Leostream pool with the name and center id passed to the function OR get the existing pool data for the pool id passed to the function.
            Steps:
            1. Get a reference to the Leostream API
            2. If the pool id is None, create a new pool via the API
            3. If the pool id is not None, get the pool data via the API
            '''
        self._api = LeostreamClient()
        if id is None:
            self._URL="https://"+str(self._api.broker)+"/rest/v1/pools/"
            # create an emtpy json object to store the data
            self.data = {
                    "name": name,
                    "pool_definition": {
                        "restrict_by": "C",
                        "server_ids": center_id,
                },
            }
            self.data = self.create()
            self._id = self.data['id']
        else:
            self._id = id
            self._URL="https://"+str(self._api.broker)+"/rest/v1/pools/"+ str(self._id)
            self.data = self.get()
               
    def update_image(self, target_image_name):
        ''' Goal: Update this Leostream pool with the image name passed to the function.
            Steps:
            1. Get the current image id for the pool
            2. Get the AMI name of the current image from it's center
            3. Compare the pool AMI name to the AMI name passed to the function
            4. If the AMI name has changed, check if the new definition exists in the center
            If the image name exist in the center, update the pool via the API'''
        
        # Placeholder for the current image
        current_image = {}

        # Get the current image id
        current_image['id'] = self.data['provision']['provision_vm_id']
        print(f"Updating pool: {current_image['id']}")

        # Get center for this pool
        center = LeostreamCenter(self.data['provision']['center']['id'])
        
        # Get the AMI name of the current image
        current_image['name'] = [x for x in center.data['images'] if x["id"] == current_image['id']][0]['name']
        print(f"Current image for pool: {current_image['name']}")

        # Compare the pool AMI name to the AMI name passed to the function
        if current_image['name'] != target_image_name:
            print(f"Current image name:{current_image['name'] } differs from target name:{target_image_name}, will update pool configuration")
            
            # Does the new definition exist in the center?
            image_in_center = [x for x in center.data['images'] if x["name"] == target_image_name]

            # If image_in_center is empty, the AMI does not exist in the center
            if image_in_center:
                print(f"{target_image_name}: Image exists in the center") 
                print(f"Updating pool image to: {image_in_center[0]['name']}")
                # Update the pool when it does exist
                data = {
                    "provision": {
                        "provision_vm_id": image_in_center[0]['id'] 
                    }
                }
                # Call the update function in the WebResource class
                self.update(data)
            else:
                print(f"{target_image_name}: Target image does not exist in the center")
        else:
            print(f"{target_image_name}:{current_image['name']} Target image from file and current pool image match, no update required")
