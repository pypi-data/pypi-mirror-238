import os

from typing import Union

class KurocoAccess:
        _access_token: str
        ACCESS_TOKEN_KEY: str = "x-rcms-api-access-token"
        ACCESS_TOKEN_ENV_KEY: str = "KUROCO_ACCESS_TOKEN"

        def __init__(self, access_token: Union[str, None] = None) -> None:
            self.access_token = access_token

        @property
        def access_token(self):
            return self._access_token
        
        @access_token.setter
        def access_token(self, value: Union[str, None]):
            if value is None:
                value = self.get_access_token_from_env()
            self._access_token = KurocoAccess.Checkers.access_token(value)

        def get_access_token_from_env(self) -> Union[str, None]:
            """
            Gets the access token from the environment variables.

            Returns:
                str: The access token from the environment variables.
            """
            return os.getenv(self.ACCESS_TOKEN_ENV_KEY)

        def add_access_token_to_headers(self, headers: dict) -> dict:
            """
            Adds the access token to the headers.

            Args:
                headers (dict): The headers to add the access token to.

            Returns:
                dict: The headers with the access token added.
            """
            headers[self.ACCESS_TOKEN_KEY] = self.access_token
            return headers

        class Checkers:
            """
            A class used to represent the checkers for the KurocoAccess class
            """ 
            @staticmethod
            def access_token(value: Union[str, None]) -> str:
                """
                Checks that the access token is a string.

                Args:
                    value (str): The access token to check.

                Returns:
                    str: The access token if it is a string.

                Raises:
                    AssertionError: If the access token is not a string.
                """
                if value is None:
                    raise AssertionError("Access token must be provided as passed argument or as environment variable")
                assert isinstance(value, str), "Access token must be a string"
                return value
            
        