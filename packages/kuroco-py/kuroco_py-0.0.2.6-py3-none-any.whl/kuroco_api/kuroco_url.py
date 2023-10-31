import os 

from typing import Union

class KurocoURL:
    _domain: str
    _version: int
    path: dict

    DOMAIN_ENV_KEY: str = "KUROCO_API_DOMAIN"
    VERSION_ENV_KEY: str = "KUROCO_API_VERSION"

    def __init__(self, domain: Union[str, None] = None, version: Union[str, int, None] = None):
        self.domain = domain
        self.version = version
        self.path = KurocoURL.get_path(self.domain, self.version, "")

    @property
    def domain(self):
        return self._domain
    
    @domain.setter
    def domain(self, value: Union[str, None]):
        if value is None:
            value = os.getenv(self.DOMAIN_ENV_KEY)
        self._domain = KurocoURL.Checkers.domain(value)

    @property
    def version(self):
        return self._version
    
    @version.setter
    def version(self, value: Union[str, int, None]):
        if value is None:
            value = os.getenv(self.VERSION_ENV_KEY, "1")
        self._version = KurocoURL.Checkers.version(value)

    class Checkers:
        """
        A class used to represent the checkers for the KurocoURL class
        """    
        @staticmethod
        def domain(value: Union[str, None]) -> str:
            """
            Checks that the API domain is a string.

            Args:
                value (str): The API domain to check.

            Returns:
                str: The API domain if it is a string.

            Raises:
                AssertionError: If the API domain is not a string.
            """
            if value is None:
                raise AssertionError("API domain must be provided as an argument or as an environment variable")
            assert isinstance(value, str), f"Domain must be a string"
            return value

        @staticmethod
        def version(value: Union[str, int]) -> int:
            """
            Converts the version to an integer.

            Args:
                value: The version to convert.

            Returns:
                int: The version as an integer.

            Raises:
                AssertionError: If the version is not an integer or not castable to integer.
            """
            assert isinstance(value, int) or int(value), f"Version must be an integer or a castable type to integer"
            return int(value)

    class Converters:
        @staticmethod  
        def version(value):
            """
            Converts the given value to an integer and returns it as a string.

            Args:
                value (Any): The value to be converted to an integer.

            Returns:
                str: The integer value as a string.
            """
            return f"{int(value)}"


    @staticmethod
    def get_path(api_domain: str, version: Union[int, str], endpoint: str) -> dict:
        """
        Get the path to the Kuroco API
        
        Parameters:
        api_domain (str): The domain of the Kuroco API
        version (int): The version of the Kuroco API
        endpoint (str): The endpoint of the Kuroco API
        
        Returns:
        str: The path to the Kuroco API
        """
        assert isinstance(api_domain, str), "API domain must be a string"
        assert isinstance(endpoint, str), "API endpoint must be a string"
        return {"domain": api_domain, "version": KurocoURL.Converters.version(version), "endpoint": endpoint}
    

    @staticmethod
    def path_maker(base: dict, *endpoint: str) -> str:
        """
        Constructs a URL path from a base dictionary and endpoint strings.

        Args:
            base (dict): A dictionary containing the base URL components.
            endpoint (str): One or more endpoint strings to append to the base URL.

        Returns:
            str: The constructed URL path.
        """
        if endpoint and endpoint[0]:
            return os.path.join(base["domain"], base["version"], base["endpoint"], *endpoint)
        else:
            return os.path.join(base["domain"])
        
    def get_path_to_endpoint(self, *endpoint: str) -> str:
        """
        Constructs a URL path from the base URL components and endpoint strings.

        Args:
            endpoint (str): One or more endpoint strings to append to the base URL.

        Returns:
            str: The constructed URL path.
        """
        return KurocoURL.path_maker(self.path, *endpoint)