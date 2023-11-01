#==============================================================================
# Class to make HTTP REST requests
# Flávio Gomes da Silva Lisboa <flavio.lisboa@fgsl.eti.br>
# https://github.com/fgsl/pyrest
#==============================================================================

import requests
import json
from json import dumps

class Rest:
    def __init__(self):
        self.requestErrors = {}
        self.requestCounter = 0
        self.baseUrl = ""
        self.dataErrors = {}
        self.methodErrors = {}
        self.method = "GET"

    # Method to make a HTTP GET request
    def doGet(self,headers,url,expectedCode,verbose=False):
        self.method = "GET"
        response = self.tryRequest(url,headers,[],verbose)
        
        return self.assertResponse(expectedCode,response,verbose,[])

    # Method to make a HTTP POST request
    def doPost(self,data,headers,url,expectedCode,verbose=False):
        self.method = "POST"
        response = self.tryRequest(url,headers,data,verbose)
        
        return self.assertResponse(expectedCode,response,verbose,data)
    
    # Method to make a HTTP DELETE request
    def doDelete(self, headers,url,expectedCode,verbose=False):
        self.method = "DELETE"        
        response = self.tryRequest(url,headers,[],verbose)
        
        return self.assertResponse(expectedCode,response,verbose,[])
    
    # Method to make a HTTP PATCH request
    def doPatch(self,data,headers,url,expectedCode,verbose=False):
        self.method = "PATCH"        
        response = self.tryRequest(url,headers,data,verbose)
        
        return self.assertResponse(expectedCode,response,verbose,data)

    def tryRequest(self,url,headers,data,verbose):
        if verbose: print("=" * 80)
        try:
            if url.find("?") > 0: self.baseUrl = url[0:url.find("?")] 
            else: self.baseUrl = url
            if verbose: print("Requesting " + self.baseUrl + " via HTTP " + self.method)
            self.requestCounter +=1
            match self.method:
                case "GET":
                    response = requests.get(url, json=data, headers=headers)
                case "POST":
                    response = requests.post(url, json=data, headers=headers)
                case "DELETE":
                    response = requests.delete(url, json=data, headers=headers)
                case "PATCH":
                    response = requests.patch(url, json=data, headers=headers)

        except requests.exceptions.HTTPError as error:
            if verbose: print("Request error!", error)
            self.requestErrors[self.baseUrl] = response.status_code
            self.methodErrors[self.baseUrl] = self.method
            self.dataErrors[self.baseUrl] = str(data)
            return ""
        except requests.exceptions.ConnectionError as error:
            if verbose: print("Connection error!", error)
            self.requestErrors[self.baseUrl] = response.status_code
            self.methodErrors[self.baseUrl] = self.method
            self.dataErrors[self.baseUrl] = str(data)
            return ""
        
        return response

    def assertResponse(self,expectedCode,response,verbose,data):
        if response.status_code != expectedCode:
            if verbose: 
                print("Expected " + str(expectedCode) + " Received " + str(response.status_code))
            self.requestErrors[self.baseUrl] = response.status_code
            self.methodErrors[self.baseUrl] = self.method
            self.dataErrors[self.baseUrl] = str(data)
        else:
            if verbose: print("Response Status OK for " + self.baseUrl)
        if verbose: print("=" * 80)
        try:
            response_json = response.json()
        except json.decoder.JSONDecodeError as error:
            if verbose: print("Parsing error!", error)
            self.requestErrors[self.baseUrl] = response.status_code
            self.methodErrors[self.baseUrl] = self.method
            self.dataErrors[self.baseUrl] = str(data)
            return response.text

        return dumps(response_json)        
