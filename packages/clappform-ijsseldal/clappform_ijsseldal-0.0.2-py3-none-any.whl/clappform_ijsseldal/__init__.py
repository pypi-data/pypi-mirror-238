"""
Clappform API Wrapper
~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022 Clappform B.V..
:license: MIT, see LICENSE for more details.
"""
__requires__ = ["requests==2.28.1", "pandas==1.5.2"]


# Metadata
__version__ = "0.0.0"
__author__ = "Clappform B.V."
__email__ = "info@clappform.com"
__license__ = "MIT"
__doc__ = "Clappform Python API wrapper"


# %%
import requests
import logging
import json
import pandas as pd
import re
import requests
import logging
import json

from bs4 import BeautifulSoup
from enum import Enum, auto
import xml.etree.ElementTree as ET
import xmltodict

# %%
class IjssedalException(Exception):
    """REST Exceptions Class"""


class IjsseldalSOAPException(Exception):
    """SOAP Exceptions Class"""

class IjssedalREST:
    # Define a list of supported endpoints with their paths and HTTP methods
    endpoints = [
        {
            "path": "Verhuurbare_objecten",
            "endpoint_id": "Ophalen van Verhuurbare Objecten",
            "method": "GET"
        },
        {
            "path": "Verhuurbare_objecten",
            "endpoint_id": "Ophalen Verhuurbare Objecten Expand op Hierarchie",
            "method": "GET",
            "extension" : "expand"
        },
        {
            "path": "Contractanten",
            "endpoint_id": "Ophalen van de contractant via Relatie_id",
            "method": "GET",
            "extension": "filter"
        },
        {
            "path": "Huurcontracten",
            "endpoint_id": "Ophalen huurcontracten via het object",
            "method": "GET",
            "extension" : "filter"
        },
        {
            "path": "Huurcontracten",
            "endpoint_id": "Huurcontracten filter op Object",
            "method": "GET",
            "extension" : "filter"
        }
    ]

    endpoint_id_mapping = {
        "Ophalen van Verhuurbare Objecten": "FetchRentalObjects",
        "Ophalen Verhuurbare Objecten Expand op Hierarchie": "FetchRentalObjectsWithHierarchy",
        "Ophalen van de contractant via Relatie_id": "FetchContractorByRelationID",
        "Ophalen huurcontracten via het object": "FetchLeasesByObjectID",
        "Huurcontracten filter op Object": "FilterLeasesByObject"
    }

    
    def __init__(self, base_url: str, client_id: str, client_secret: str, username: str, password: str, headers: dict, timeout: int = 10):
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.headers = headers
        self.timeout = timeout

    def get_auth_token(self) -> str:
        """Retrieve the authentication token."""
        response = requests.request(
            "POST",
            f"{self.base_url}/vip/login?grant_type=password&client_id={self.client_id}&client_secret={self.client_secret}&username={self.username}&password={self.password}",
            timeout=self.timeout
        )
        if response.status_code != 200:
            raise IjssedalException("Failed to retrieve authentication token!")
        return response.json()["access_token"]

    def __add_filter(self, filters: str):
        """Add filter to the base URL."""
        if not filters:
            return ""
        # filter_parts = [f"{k}={p}" for k, p in filters.items()]
        # return "?" + "&".join(filter_parts)
        # # return f"?{filters}" if filters else ""
        # Create the URL components based on the filters dictionary
        filter_parts = []
        for k, p in filters.items():
            # If filter key matches certain names like 'expand', 'skip', etc. prefix with `$`.
            if k in ['expand', 'skip', 'filter', 'orderby']:  # You can extend this list for other OData parameters
                filter_parts.append(f"${k}={p}")
            else:
                filter_parts.append(f"{k}={p}")
    
        # Join the components with `&` and prefix with `?`
        return "?" + "&".join(filter_parts)


    def fetch_data_from_endpoint(self, endpoint_id: str, filters: dict = None) -> list:
        """Fetch data from the specified OData endpoint."""

        # Translate the English endpoint ID back to the original one
        translated_endpoint_id = next((key for key, value in self.endpoint_id_mapping.items() if value == endpoint_id), None)
        if not translated_endpoint_id:
            raise IjssedalException(f"Endpoint '{endpoint_id}' translation not found!")
    
        # Search for the translated endpoint ID in the endpoints list
        endpoint = next((e for e in self.endpoints if e["endpoint_id"] == translated_endpoint_id), None)

        if not endpoint:
            raise IjssedalException(f"Endpoint '{translated_endpoint_id}' not found!")
    
        # Initial URL
        url = f"{self.base_url}/{endpoint['path']}{self.__add_filter(filters)}"
        
        print(f"Constructed URL: {url}")

        # Extract skip value if provided in filters
        initial_skip = int(filters.get("$skip", 0))


        return self.__fetch_odata_data(url, initial_skip)

    def __fetch_odata_data(self, url: str, skip: int = 0) -> list:
        """Helper method to recursively fetch OData paginated data."""
        
        # Merge the Authorization token with the provided headers
        headers_with_token = self.headers.copy()
        headers_with_token['Authorization'] = f"Bearer {self.get_auth_token()}"
        
        # Check if $skip is already in the URL, then update its value; otherwise, append it.
        if "$skip=" in url:
            url = re.sub(r"\$skip=\d+", f"$skip={skip}", url)
        else:
            separator = "&" if "?" in url else "?"
            url = f"{url}{separator}$skip={skip}"
        
        response = requests.get(url, headers=headers_with_token, timeout=self.timeout)
        print(url)
        
        if response.status_code > 204:
            print(response.text)
            print("Request URL:", url)  
            raise IjssedalException(f"Failed to fetch data! HTTP Status Code: {response.status_code}")
            
        if response.status_code == 200:
            data = response.json().get('value', [])
            
            if not data:  # If no data is returned, simply return an empty list
                return []
            
            skip = skip + len(data)
            data_loop = self.__fetch_odata_data(url, skip)  # Recursively fetch next page's data, updating the skip value
            
            if data_loop:
                data.extend(data_loop)
            
            return data
        elif response.status_code == 204:
            logging.info("Reached end of loop")
            return []
        
        raise IjssedalException(f"Uncaught error")
    
    def fetch_data_as_dataframe(self, endpoint_id: str, filters: dict = None) -> pd.DataFrame:
        """Fetch data from the specified OData endpoint and return as a pandas DataFrame."""
        data = self.fetch_data_from_endpoint(endpoint_id, filters)
        return pd.DataFrame(data)
    
class IjsseldalSOAP:
        
    # Define a list of supported endpoints with their paths and HTTP methods
        endpoints = [
            {
                "endpoint_id": "GetCases",
                "method": "POST"
            },
            {
                "endpoint_id": "GetCaseStartState",
                "method": "POST"
            }
        ]

        def __init__(self, base_url_login: str, base_url: str, username: str, password: str, soap_userid: str, plain_passwd: str, headers: dict, timeout: int):
            self.base_url_login = base_url_login
            self.base_url = base_url
            self.username = username
            self.password = password
            self.soap_userid = soap_userid
            self.plain_passwd = plain_passwd
            self.headers = headers
            self.timeout = timeout

        def get_session_id(self ) -> str:
            # Generate XML for session ID retrieval
            xml = f"""<soapenv:Envelope 
            xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
            xmlns:cal="http://xml.itris.nl/viewpoint/2010/09/23/calls" 
            xmlns:ih="http://xml.itris.nl/viewpoint/2009/01/29/soap-header">
                <soapenv:Header>
                    <ih:soapuserid>{self.soap_userid}</ih:soapuserid>
                    <ih:plainpasswd>{self.plain_passwd}</ih:plainpasswd>
                </soapenv:Header>
                <soapenv:Body>
                    <cal:impersonate>
                        <cal:username>{self.username}</cal:username>
                        <cal:password>{self.password}</cal:password>
                    </cal:impersonate>
                </soapenv:Body>
            </soapenv:Envelope>"""
            response = requests.post(self.base_url_login, data=xml, headers=self.headers, timeout=self.timeout)
            text_response = response.text
            soup = BeautifulSoup(text_response, 'lxml-xml')
            # Extract sessionId and return it
            session_id = soup.find('F:sessionId').text
            return session_id

        def get_case_start_state(self, caseTypeDefinitionId: str) -> str:
            qParams = {"caseTypeDefinitionId": caseTypeDefinitionId}
            response = self.call_endpoint("GetCaseStartState", qParams)
            return response


        def generate_soap_request(self, qParams: dict) -> str:
            header = self.generate_soap_header()
            body = self.generate_soap_body(qParams)

            envelope = f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap="http://xml.itris.nl/viewpoint/2016/01/01/soap-header" xmlns:data="http://cad.soap.itris.nl/2016/01/01/calls/data">
            {header}
            {body}
            </soapenv:Envelope>"""

            return envelope

        def generate_soap_header(self):
            session_id = self.get_session_id()
            messageUID = "fdas-adsfaf-asd-f-ad-f"
            relatedMessageUID = "2020-12-01T00:00:00Z"
            messageCreatedDate = "2020-12-01T00:00:00Z"

            header = f"""
            <soapenv:Header>
                <soap:MessageIdentification>
                    <soap:messageUID>{messageUID}</soap:messageUID>
                    <!--Optional:-->
                    <soap:relatedMessageUID>{relatedMessageUID}</soap:relatedMessageUID>
                    <soap:messageCreatedDate>{messageCreatedDate}</soap:messageCreatedDate>
                </soap:MessageIdentification>
                <soap:BasicSecurity>
                    <soap:username>{self.soap_userid}</soap:username>
                    <soap:password>{self.password}</soap:password>
                    <soap:sessionId>{session_id}</soap:sessionId>
                </soap:BasicSecurity>
            </soapenv:Header>
            """
            return header

        def generate_soap_body(self, qParams: dict) -> str:
            if "caseTypeDefinitionId" in qParams:
                # Check if the request is for GetCaseStartState
                if "startDate" in qParams or "endDate" in qParams or "status" in qParams:
                    return self.generate_get_cases_body(qParams)
                else:
                    return self.generate_get_case_start_state_body(qParams)
            else:
                raise IjsseldalSOAPException("Missing 'caseTypeDefinitionId' in qParams")



        def generate_get_cases_body(self, qParams: dict) -> str:
            caseTypeDefinitionId_tag = f"<data:caseTypeDefinitionId>{qParams['caseTypeDefinitionId']}</data:caseTypeDefinitionId>"
            startDate_tag = f"<data:startDate>{qParams['startDate']}</data:startDate>"

            # Conditionally include endDate and status elements if provided
            endDate = qParams.get('endDate')
            if endDate:
                endDate_tag = f"<data:endDate>{endDate}</data:endDate>"
            else:
                endDate_tag = ""

            status = qParams.get('status')
            if status:
                status_tag = f"<data:status>{status}</data:status>"
            else:
                status_tag = ""

            body = f"""
            <soapenv:Body>
                <data:GetCases>
                    {caseTypeDefinitionId_tag}
                    {startDate_tag}
                    {endDate_tag}
                    {status_tag}
                </data:GetCases>
            </soapenv:Body>
            """
            return body

        def generate_get_case_start_state_body(self, qParams: dict) -> str:
            caseTypeDefinitionId = qParams['caseTypeDefinitionId']

            body = f"""
            <soapenv:Body>
                <data:GetCaseStartState>
                    <data:caseTypeDefinitionId>{caseTypeDefinitionId}</data:caseTypeDefinitionId>
                </data:GetCaseStartState>
            </soapenv:Body>
            """
            return body

        def call_endpoint(self, endpoint_id: str, qParams: dict) -> str:
            # Find the endpoint details based on endpoint_id
            endpoint = next((e for e in self.endpoints if e["endpoint_id"] == endpoint_id), None)

            if not endpoint:
                raise IjsseldalSOAPException(f"Endpoint '{endpoint_id}' not found")

            # Generate the SOAP request
            soap_request = self.generate_soap_request(qParams)
            # print("SOAP Request:")
            # print(soap_request)

            response = requests.post(self.base_url, data=soap_request, headers=self.headers, timeout=self.timeout)

            if response.status_code != 200:
                raise IjsseldalSOAPException("Failed to retrieve data from the API")

            # return response.text
            return self.transform_response_to_json(response.content.decode('utf-8'))


        def transform_response_to_json(self, response: str) -> dict:
            # Find the start of the XML content
            start_index = response.find('<soap:Envelope')
            end_index = response.rfind('</soap:Envelope>') + len('</soap:Envelope>')

            # Check if both start and end tags are found
            if start_index == -1 or end_index == -1:
                raise IjsseldalSOAPException("Could not find proper XML content in the response")

            # Extract the XML content
            extracted_response = response[start_index:end_index + 1]

            # Convert XML to dictionary
            data_dict = xmltodict.parse(extracted_response)

            # Remove data: prefix
            cleaned_data_dict = self.remove_data_prefix(data_dict)

            return cleaned_data_dict

        def remove_data_prefix(self, data_dict):
            if isinstance(data_dict, dict):
                new_dict = {}
                for key, value in data_dict.items():
                    new_key = re.sub(r'^data:', '', key)
                    new_value = self.remove_data_prefix(value)
                    new_dict[new_key] = new_value
                return new_dict
            elif isinstance(data_dict, list):
                return [self.remove_data_prefix(item) for item in data_dict]
            else:
                return data_dict

class IjssedalWrapper:
    def __init__(self, 
                 rest_base_url: str, rest_client_id: str, rest_client_secret: str, rest_username: str, rest_password: str, rest_headers: dict, rest_timeout: int,
                 soap_base_url_login: str, soap_base_url: str, soap_username: str, soap_password: str, soap_userid: str, soap_plain_passwd: str, soap_headers: dict, soap_timeout: int):
        self.rest = IjssedalREST(
            base_url=rest_base_url,
            client_id=rest_client_id,
            client_secret=rest_client_secret,
            username=rest_username,
            password=rest_password,
            headers=rest_headers,
            timeout=rest_timeout
        )
        self.soap = IjsseldalSOAP(
            base_url_login=soap_base_url_login,
            base_url=soap_base_url,
            username=soap_username,
            password=soap_password,
            soap_userid=soap_userid,
            plain_passwd=soap_plain_passwd,
            headers=soap_headers,
            timeout=soap_timeout
        )

