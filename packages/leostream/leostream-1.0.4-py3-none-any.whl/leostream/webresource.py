# pylint: disable=E1101
import requests
import json
from .restapi import LeostreamClient

class WebResource(object):
    ''' This class is the base class for all Leostream resources found in the API. It contains the common functions
        for all resources. 

        # General design ideas for the WebResource class

        There are two types of methods: class methods and instance methods

        ## For the class methods:
        The base class has a 
        * list method that will return a list of all resources of the resource_type specified in the url attribute
        * find method that will find the resource for the name passed to the function.

        The child class will have a   
        * resource_type attribute that contains the name/type of the resource
        * some classes can override the base class methods(like list()  or find() ) to add additional functionality -- see poolassignment.py

        ## For the instance methods:
        The object will have a
        * data attribute that contains the data from the API
        * _URL attribute that contains the URL for the resource
        * _HEADERS attribute that contains the headers for the resource
        * _api attribute that contains the LeostreamClient singleton object
        * get() function that will return the data from the API
        * update() function that will update the resource via the API
        * create() function that will create the resource via the API (TODO not implemented fully)

        Rationale for design:
        - Create classes for Leostream entities like Pools, Centers, Gateways etc.
        - Group common classes in a Package
        - Each class is responsible for it's own data
        - Create inheritance relation or interface like construction to avoid duplication (login to Leostream/ API get,update)
        '''
    
    @classmethod
    def list(cls):
        '''
        This method will return a list of all resources of the type specified in the url attribute'''

        cls._api = LeostreamClient()
        cls._HEADERS = {
        'Content-Type':'application/json',
        'Authorization': cls._api._session}
        cls._URL="https://"+str(cls._api.broker)+"/rest/v1/" + cls.resource_type + "?as+tree=0"
        
        response = requests.get(url=cls._URL, headers=cls._HEADERS, verify=False)
        data = response.json()

        # check https status code
        if response.status_code != 200:
            raise Exception("Error: the request returned HTTP status code " + str(response.status_code) + " with the following message: " + str(data))

        return data

    @classmethod
    def find(cls, name):
        ''' Goal: Find the resource for the resource name passed to the function.
            Steps:
            1. Get the list of resources for the resource type 
            2. Filter the list with the resource name passed to the function
            3. Return the resource found'''
        
        # Get the he current resource by name       
        cls.data = cls.list()
        resource = [x for x in cls.data if x["name"]==name]
        # If the resource is not found, raise an exception
        if not resource:
            raise Exception(f"Error: Resource {name} not found")
        else:
            return resource

    def create(self):
        '''
        This method will create the resource via the API. It will return the response from the API'''
        
        self._HEADERS = {
        'Content-Type':'application/json',
        'Authorization': self._api._session}

        response = requests.post(url=self._URL, headers=self._HEADERS, verify=False, data=json.dumps(self.data))
        data = response.json()

        # check https status code
        if response.status_code != 201:
            raise Exception("Error: the request returned HTTP status code " + str(response.status_code) + " with the following message: " + str(data))

        return data['stored_data']
         
    def update(self , data):
        ''' 
        This method will update the resource via the API. It will return the response from the API'''

        self._HEADERS = {
        'Content-Type':'application/json',
        'Authorization': self._api._session}

        response = requests.put(url=self._URL, headers=self._HEADERS, verify=False, data=json.dumps(data))
        data = response.json()

        # check https status code
        if response.status_code != 200:
            raise Exception("Error: the login request returned HTTP status code " + str(response.status_code) + " with the following message: " + str(data))

        return data
    
    def get(self):
        '''
        This method will return the data for the resource specified in the url attribute'''

        self._HEADERS = {
        'Content-Type':'application/json',
        'Authorization': self._api._session}

        response = requests.get(url=self._URL, headers=self._HEADERS, verify=False)
        data = response.json()

        # check https status code
        if response.status_code != 200:
            raise Exception("Error: the request returned HTTP status code " + str(response.status_code) + " with the following message: " + str(data))

        return data
