import aiohttp
import asyncio
import logging
import json
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from urllib.parse import quote
from typing import List, Dict, Union
from dataclasses import dataclass

from .kuroco_response import KurocoResponse
from .kuroco_access import KurocoAccess
from .kuroco_url import KurocoURL
from .CONFIG import KUROCO_ACCESS_TOKEN, KUROCO_API_DOMAIN, KUROCO_API_VERSION


GET_KW: str = "GET"
POST_KW: str = "post"
PUT_KW: str = "POST"
DELETE_KW: str = "POST"

KEYS_FOR_INIT: List[str] = [
    KUROCO_ACCESS_TOKEN,
    KUROCO_API_DOMAIN,
    KUROCO_API_VERSION
]

@dataclass
class KurocoAPI:
    """
    A class used to represent a KurocoAPI object
    
    Attributes:
    access_token (str): The access token used for Kuroco API requests
    endpoint (str): The endpoint used for Kuroco API requests
    version (str): The version used for Kuroco API requests
    
    Note:
    The access token must be set before making any Kuroco API requests
    This object is used to make Kuroco API requests from a unique version of the API. To use multiple versions, then create multiple KurocoAPI objects

    Examples:
    >>> api = KurocoAPI("ACCESS_TOKEN", "test.api.com", 1)
    
    >>> api = KurocoAPI()
    >>> api.post("test", {"test": "test"})
    """
    _kuroco_access: KurocoAccess
    _kuroco_url: KurocoURL

    def __init__(self, access_token: Union[str, None] = None, api_domain: Union[str, None] = None, api_version: Union[str, int, None] = None) -> None:
        """
        Parameters:
        access_token (str): The access token used for Kuroco API requests
        api_domain (str): The domain of the Kuroco API
        api_version (int): The version of the Kuroco API

        Note:
        The access token must be set before making any Kuroco API requests        
        """
        self._kuroco_access = KurocoAccess(access_token=access_token)
        self._kuroco_url = KurocoURL(domain=api_domain, version=api_version)

    @classmethod
    def load_from_file(cls, path: str) -> 'KurocoAPI':
        """
        Load the Kuroco API from a configuration file

        Parameters:
        path (str): The path to the file containing the Kuroco API configuration as json

        Returns:
        None
        """
        values_for_init = {}
        with open(path) as f:
            values = json.load(f)
            values_for_init = {str(k).replace("KUROCO_", "").lower(): v for k, v in values.items() if k in KEYS_FOR_INIT}
        return cls(**values_for_init)
    
    @property
    def version(self):
        return self._kuroco_url.version

    async def get_endpoints(self) -> List[Dict]:
        """
        Get all endpoints for the Kuroco API

        Returns:
        list: A list of all endpoints for the Kuroco API and their definitions
        """
        # TODO: Implement
        pass

    @staticmethod
    async def call(url, method=GET_KW, params=None, data=None, headers=None) -> KurocoResponse:
        """
        Sends an HTTP request to the specified URL using the specified method, parameters, data, and headers.

        Args:
            url (str): The URL to send the request to.
            method (str, optional): The HTTP method to use for the request. Defaults to GET_KW.
            params (dict, optional): The query parameters to include in the request. Defaults to None.
            data (dict, optional): The request body data to include in the request. Defaults to None.
            headers (dict, optional): The headers to include in the request. Defaults to None.

        Returns:
            KurocoResponse: The response from the server.
        """
        logger.info("[%s] URL: %s", method.upper(), url)
        if params:
            params = {k: quote(v) if isinstance(v, str) else v for k, v in params.items() if v is not None}
        s_time = time.time()
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, params=params, data=data, headers=headers) as response:
                if response.status < 400:
                    elapsed_time =  time.time() - s_time
                    logger.info(
                        "[%s] URL: %s, Status: %s, Latency: %.3f s",
                        method.upper(),
                        url,
                        response.status,
                        elapsed_time,
                    )
                    return KurocoResponse(response.status, await response.json())
                else:
                    logger.error(f"Error: {response.status}, {await response.text()}")
                    return KurocoResponse(response.status, await response.text())
    
    async def call_send(self, url, method=GET_KW, params=None, data=None, headers=None) -> KurocoResponse:
        """
        Sends a request to the specified URL using the specified method, parameters, data, and headers.
        
        Args:
            url (str): The URL to send the request to.
            method (str, optional): The HTTP method to use for the request. Defaults to GET_KW.
            params (dict, optional): The query parameters to include in the request. Defaults to None.
            data (dict, optional): The request body data to include in the request. Defaults to None.
            headers (dict, optional): The headers to include in the request. Defaults to None.
        
        Returns:
            KurocoResponse: The response from the server.
        
        Note:
            Adds an access token to the headers if one is not already present.
            Converts the data to JSON format if it is provided.
            Sets the Content-Type header to "application/json".
        """
        headers = self._kuroco_access.add_access_token_to_headers(headers or {})
        if data:
            data = json.dumps(data)
        headers["Content-Type"] = "application/json"
        return await KurocoAPI.call(url, method, params, data, headers)

    @staticmethod
    def call_sync(url, method=GET_KW, params=None, data=None, headers=None) -> KurocoResponse:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(KurocoAPI.call(url, method, params, data, headers))

    def call_send_sync(self, url, method=GET_KW, params=None, data=None, headers=None) -> KurocoResponse:
        headers = self._kuroco_access.add_access_token_to_headers(headers or {})
        if data:
            headers["Content-Type"] = "application/json"
            data = json.dumps(data)
        return KurocoAPI.call_sync(url, method, params, data, headers)

    async def post(self, url: str, params: dict = None, data: object = None, no_auto_domain: bool = False) -> KurocoResponse:
        """"
        Make a post request to the Kuroco API
        
        Parameters:
        url (str): The url to make the post request to
        params (dict): The parameters to be sent with the post request
        data (object): The data to be sent with the post request#
        no_auto_domain (bool): Whether to automatically add the api domain to the url
            
        Returns:
        None

        Note:
        The access token is automatically added
        This method is async, so it must be awaited. Use post_sync for a synchronous version
        """
        if not no_auto_domain:
            url = self._kuroco_url.get_path_to_endpoint(url)
        return await self.call_send(url=url, method=POST_KW, params=params, data=data)

    def post_sync(self, url: str, params: dict = None, data: object = None, no_auto_domain: bool = False) -> KurocoResponse:
        """"
        Make a post request to the Kuroco API
        
        Parameters:
        url (str): The url to make the post request to
        params (dict): The parameters to be sent with the post request
        data (object): The data to be sent with the post request#
        no_auto_domain (bool): Whether to automatically add the api domain to the url
            
        Returns:
        None

        Note:
        The access token is automatically added
        This method is synchronous, so it must not be awaited. Use post for an asynchronous version
        """
        if not no_auto_domain:
            url = self._kuroco_url.get_path_to_endpoint(url)
        return self.call_send_sync(url=url, method=POST_KW, params=params, data=data)

    async def get(self, url: str, params: dict, no_auto_domain: bool = False) -> KurocoResponse:
        """
        Make a get request to the Kuroco API

        Parameters:
        url (str): The url to make the get request to
        params (dict): The parameters to be sent with the get request
        no_auto_domain (bool): Whether to automatically add the api domain to the url

        Returns:
        None

        Note:
        The access token is automatically added to the params
        This method is async, so it must be awaited. Use get_sync for a synchronous version
        """
        if "filter" in params:
            if not params["filter"]:
                del params["filter"]
            else:
                # Format filter as string
                params["filter"] = "&".join([f"{k}={v}" for k, v in params["filter"].items()])
                # Remove top &
                params["filter"] = params["filter"][1:]
        if not no_auto_domain:
            url = self._kuroco_url.get_path_to_endpoint(url)
        return await self.call_send(url, GET_KW, params)

    def get_sync(self, url: str, params: dict, no_auto_domain: bool = False) -> KurocoResponse:
        """
        Make a get request to the Kuroco API

        Parameters:
        url (str): The url to make the get request to
        params (dict): The parameters to be sent with the get request
        no_auto_domain (bool): Whether to automatically add the api domain to the url

        Returns:
        None

        Note:
        The access token is automatically added to the params
        This method is synchronous, so it must not be awaited. Use get for an asynchronous version
        """
        if not no_auto_domain:
            url = self._kuroco_url.get_path_to_endpoint(url)
        return self.call_send_sync(url, GET_KW, params)

    async def put(self, url: str, key: str, params: dict = None, data: object = None, no_auto_domain: bool = False) -> KurocoResponse:
        """
        Make a put request to the Kuroco API

        Parameters:
        url (str): The url to make the put request to
        params (dict): The parameters to be sent with the put request
        data (object): The data to be sent with the put request
        no_auto_domain (bool): Whether to automatically add the api domain to the url

        Returns:
        None

        Note:
        The access token is automatically added to the params
        This method is async, so it must be awaited. Use put_sync for a synchronous version
        """
        if not no_auto_domain:
            url = self._kuroco_url.get_path_to_endpoint(url, key)
        return await self.call_send(method=PUT_KW, url=url, params=params, data=data)

    def put_sync(self, url: str, key: str, params: dict = None, data: object = None, no_auto_domain: bool = False) -> KurocoResponse:
        """
        Make a put request to the Kuroco API

        Parameters:
        url (str): The url to make the put request to
        params (dict): The parameters to be sent with the put request
        data (object): The data to be sent with the put request
        no_auto_domain (bool): Whether to automatically add the api domain to the url

        Returns:
        None

        Note:
        The access token is automatically added to the params
        This method is synchronous, so it must not be awaited. Use put for an asynchronous version
        """
        if not no_auto_domain:
            url = self._kuroco_url.get_path_to_endpoint(url, key)
        return self.call_send_sync(method=PUT_KW, url=url, params=params, data=data)

    async def delete(self, url: str, key: str, no_auto_domain: bool = False) -> KurocoResponse:
        """
        Make a delete request to the Kuroco API

        Parameters:
        url (str): The url to make the delete request to
        key (str): The key to make the delete request to
        no_auto_domain (bool): Whether to automatically add the api domain to the url

        Returns:
        None

        Note:
        The access token is automatically added to the params
        This method is async, so it must be awaited. Use delete_sync for a synchronous version
        """
        if not no_auto_domain:
            url = self._kuroco_url.get_path_to_endpoint(url, key)
        return await self.call_send(url, DELETE_KW, {})
    
    def delete_sync(self, url: str, key: str, no_auto_domain: bool = False) -> KurocoResponse:
        """
        Make a delete request to the Kuroco API

        Parameters:
        url (str): The url to make the delete request to
        key (str): The key to make the delete request to
        no_auto_domain (bool): Whether to automatically add the api domain to the url

        Returns:
        None

        Note:
        The access token is automatically added to the params
        This method is synchronous, so it must not be awaited. Use delete for an asynchronous version
        """
        if not no_auto_domain:
            url = self._kuroco_url.get_path_to_endpoint(url, key)
        return self.call_send_sync(url, DELETE_KW, {})
