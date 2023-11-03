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


import requests
import logging
import json


class RudholmException(Exception):
    """Integration Exceptions Class"""

class RudholmTrims:
    # Define a list of supported endpoints with their paths and HTTP methods
    endpoints = [
        {
            "path":"AdditionalInformationsss",
            "endpoint_id":"additional_information",
            "method": "GET"
        },
        {
            "path":"AdditionalWashSymbols",
            "endpoint_id":"additional_washsymbols",
            "method": "GET"
        },
        {
            "path":"Compositions",
            "endpoint_id":"compositions",
            "method": "GET"
        },
        {
            "path":"Labels",
            "endpoint_id":"all_labels",
            "method": "GET"
        },
        {
            "path":"Labels/extended",
            "endpoint_id":"all_labels_extended",
            "method": "GET"
        },
        {
            "path":"Labels",
            "endpoint_id":"one_label_extended",
            "method": "GET",
            "path_extension": "extended"
        },
        {
            "path":"Labels",
            "endpoint_id":"one_label_update",
            "method": "PUT",
        },
        {
            "path":"Labels",
            "endpoint_id":"one_label_delete",
            "method": "DELETE",
        },
        {
            "path":"Labels",
            "endpoint_id":"one_label_create",
            "method": "POST",
        },
        {
            "path":"Materials",
            "endpoint_id":"materials",
            "method": "GET",
        },
        {
            "path":"Suppliers",
            "endpoint_id":"suppliers",
            "method": "GET",
        },
        {
            "path":"Suppliers",
            "endpoint_id":"supplier_update",
            "method": "PUT",
        },
        {
            "path":"Suppliers",
            "endpoint_id":"supplier_create",
            "method": "POST",
        },
        {
            "path":"Templates",
            "endpoint_id":"templates",
            "method": "GET",
        },
        {
            "path":"WashInstructions",
            "endpoint_id":"washinstructions",
            "method": "GET",
        },
        {
            "path":"WashSymbols",
            "endpoint_id":"washsymbols",
            "method": "GET",
        }
    ]

    def __init__(self, url: str, headers: dict, version: str = "v1", timeout: int = 5):
        """Initialize the RudholmTrims client.

        Args:
            url (str): Base URL of the Rudholm API.
            headers (dict): Headers to be included in API requests.
            version (str, optional): API version. Defaults to "v1".
            timeout (int, optional): Request timeout in seconds. Defaults to 5.
        """
        self.headers = headers
        self.timeout = timeout
        self.base_url = f"https://{url}/api/{version}"

    def __get_endpoint(self, endpoint_id: str) -> dict:
        """Find and retrieve information about a specific endpoint.

        Args:
            endpoint_id (str): Identifier for the desired endpoint.

        Returns:
            dict: Information about the endpoint.
        """
        endpoint = next(
            (item for item in self.endpoints if item["endpoint_id"] == endpoint_id),
            None,
        )
        if endpoint is None:
            logging.error("%s not found in supported endpoints.", endpoint_id)
            raise RudholmException()  # Define the Rudholm Exception class
        return {} if endpoint is None else endpoint
    
    def __add_url_segment(self, base_url: str, segment: str):
        """Add a URL segment to the base URL if the segment is not empty.

        Args:
            base_url (str): The base URL to which the segment may be added.
            segment (str): The segment to be added to the URL.

        Returns:
            str: The updated URL with the added segment.
        """
        if segment:
            return f"{base_url}/{segment}"
        else:
            return base_url
    
    def __add_query_parameter(self, base_url: str, parameter_name: str, parameter_value: str):
        """Add a query parameter to the base URL if the parameter value is not empty.

        Args:
            base_url (str): The base URL to which the query parameter may be added.
            parameter_name (str): The name of the query parameter.
            parameter_value (str): The value of the query parameter.

        Returns:
            str: The updated URL with the query parameter.
        """
        if parameter_value:
            return f"{base_url}?{parameter_name}={parameter_value}"
        else:
            return base_url

        
    def __build_api_url(
        self, endpoint_id: str, item_id: str = "", po: str = "", sku: str = ""
    ) -> str:
        """Generate the complete URL for a specific endpoint.

        Args:
            endpoint_id (str): Identifier for the desired endpoint.
            item_id (str, optional): Identifier for an optional ID. Defaults to "".
            po (str, optional): Purchase order number. Defaults to "".
            sku (str, optional): SKU number. Defaults to "".

        Returns:
            str: Complete URL for the API request.
        """
        endpoint = self.__get_endpoint(endpoint_id)
        partial_url = f"{self.base_url}/{endpoint['path']}"

        # Add optional query parameters like 'po' and 'sku'
        partial_url = self.__add_query_parameter(partial_url, "purchaseOrderNumber", po)
        partial_url = self.__add_query_parameter(partial_url, "sku", sku)

        # Add the item_id if provided
        partial_url = self.__add_url_segment(partial_url, item_id)

        # Finally, for each route, determine if some additional specification is needed, like 'extended'
        partial_url = self.__add_url_segment(partial_url, endpoint.get('path_extension', ''))
        method = endpoint['method']
        
        logging.debug("Generated URL: %s with method %s", partial_url, method)
        return {
            'partial_url': partial_url,
            'method': method
        }

    def __fetch_data(
            self,
            base_url: str,
            method: str,
            body: dict = {}
        ) -> list:
        """Send an API request and fetch the data.

        Args:
            base_url (str): Complete URL for the API request.
            method (str): HTTP method (GET, PUT, POST, DELETE).
            body (dict, optional): Request body for POST and PUT requests. Defaults to {}.

        Returns:
            list: A list containing response information (response_code, response_data).
        """
        data = {
            'response_code': 0,
            'response_data': ""
        }

        logging.debug("API URL: %s", base_url)

        response = requests.request(method, base_url, headers=self.headers, json=body)

        data['response_code'] = response.status_code

        try:
            data['response_data'] = response.json()
        except json.JSONDecodeError as e:
            logging.debug("Failed to decode response for URL: %s", base_url)

        return data

    def fetch_all(
            self,
            endpoint_id: str,
        ) -> list:
        """Fetch data from an endpoint with no specific item ID.

        Args:
            endpoint_id (str): Identifier for the desired endpoint.

        Returns:
            list: A list containing response information (response_code, response_data).
        """
        request_url = self.__build_api_url(endpoint_id=endpoint_id)
        return self.__fetch_data(request_url['partial_url'], request_url['method'])

    def fetch_one(self, endpoint_id: str, item_id: str, body: dict = {}) -> list:
        """Fetch data for a specific item from an endpoint.

        Args:
            endpoint_id (str): Identifier for the desired endpoint.
            item_id (str): Identifier for the specific item.
            body (dict, optional): Request body for POST and PUT requests. Defaults to {}.

        Returns:
            list: A list containing response information (response_code, response_data).
        """
        request_url = self.__build_api_url(
            endpoint_id=endpoint_id, item_id=item_id
        )

        return self.__fetch_data(request_url['partial_url'], request_url['method'], body)

    def fetch_all_parameters(self, endpoint_id: str, po: str = "", sku: str = "") -> list:
        """Fetch data from an endpoint with optional query parameters.

        Args:
            endpoint_id (str): Identifier for the desired endpoint.
            po (str, optional): Purchase order number. Defaults to "".
            sku (str, optional): SKU number. Defaults to "".

        Returns:
            list: A list containing response information (response_code, response_data).
        """
        request_url = self.__build_api_url(
            endpoint_id=endpoint_id, po=po, sku=sku
        )

        return self.__fetch_data(request_url['partial_url'], request_url['method'])



