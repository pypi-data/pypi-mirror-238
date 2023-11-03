from .restapi import LeostreamClient
from .webresource import WebResource
import requests

class LeostreamPoolAssignment(WebResource):
    
    resource_type = "pool-assignments"

    def __init__(self, policy_id, id) -> None:
        ''' Goal: Get the pool assignment for the policy id and pool assignment id passed to the function.'''
        self._api = LeostreamClient()
        self._id = id
        self._policy_id = policy_id
        self._URL="https://"+str(self._api.broker)+"/rest/v1/policies/"+ str(self._policy_id) + "/pool-assignments/" + str(self._id)
        self.data = self.get()

    @classmethod
    def list(cls, policy_id):
        ''' Goal: List all pool assignments for a policy.
            Steps:
            1. Get the policy id as argument
            2. Get the pool assignments for the policy by calling the API
            3. Return the pool assignments '''

        cls._api = LeostreamClient()
        cls._HEADERS = {
        'Content-Type':'application/json',
        'Authorization': cls._api._session}
        cls._URL="https://"+str(cls._api.broker)+"/rest/v1/policies/" + str(policy_id) + "/" + cls.resource_type
        response = requests.get(url=cls._URL, headers=cls._HEADERS, verify=False)
        data = response.json()

        # check https status code
        if response.status_code != 200:
            raise Exception("Error: the request returned HTTP status code " + str(response.status_code) + " with the following message: " + str(data))

        return data
