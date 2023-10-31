import asyncio
import os

from typing import List, Tuple, Union
from functools import wraps
import pandas as pd
from kuroco_api import KurocoAPI, KurocoResponse

from .CONFIG import QUERY_KW, SCORE_DISTANCE_COLUMN_NAME


def check_params_types(types: dict):
    """
    Decorator that checks the types of the parameters of the decorated function

    Parameters:
    types (dict): The types of the parameters to check, keys are the names of the parameters and values are the types

    Returns:
    None

    Raises:
    AssertionError: If the types of the parameters are not correct
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            assert 'params' in kwargs, "Params argument not found"
            params = kwargs['params']
            assert isinstance(params, dict), "Params must be a dict"
            for key, value in types.items():
                assert key in params, f"Key {key} not found in params"
                assert isinstance(params[key], value), f"Key {key} must be of type {value} (it is {type(params[key])})"
            return func(*args, **kwargs)
        return wrapper
    return decorator


def prepare_request(path: str, params: dict, limit: int = 10) -> dict:
    """
    Prepare the request to be sent to the Kuroco API

    Parameters:
    path (str): The path to the Kuroco API
    params (dict): The parameters to be sent with the get request, must contain the query
    limit (int): The maximum number of entries to return, 0 for all

    Returns:
    tuple: The request to be sent to the Kuroco API and its parameters (path, params)
    """
    assert isinstance(params, dict), "Params must be a dict"
    assert QUERY_KW in params, "Raw Query must be provided in params"
    assert isinstance(limit, int), "Limit must be an integer"
    data = {}
    query_path: str = os.path.join(path)

    if limit > 0:
        params = {} if params is None else params
        params["limit"] = limit

    return {"url": query_path, "params": params, "data": data}


@check_params_types({ "filter": (dict, None)})
async def send_queries(paths: Union[List[str], Tuple[str]], kuroco_handler: KurocoAPI, params: dict, limit: int = 10, threshold: float = 0.0):
    """
    Send multiple queries to the Kuroco API for embedding

    Parameters:
    paths (list | tuple): The paths to the Kuroco API
    kuroco_handler (KurocoAPI): The KurocoAPI object used for Kuroco API requests
    params (dict): The parameters to be sent with the get request
    limit (int): The maximum number of entries to return, 0 for all

    Returns:
    DataFrame: A dataframe of embedded entries similar to the query in multiple queries specified in paths
    """
    k_responses = await asyncio.gather(*[send_query(path, kuroco_handler, params, limit) for path in paths])
    values = pd.DataFrame(pd.concat(response.data for response in k_responses)).sort_values(SCORE_DISTANCE_COLUMN_NAME, ascending=True)
    # Deal with limit of multiple calls (limit only managed on server side for one call)
    if limit > 0 and len(values) > limit:
        values = values.drop(values.index[limit:])
    return values if threshold <= 0.0 else values.loc[values[SCORE_DISTANCE_COLUMN_NAME] <= threshold]


async def send_query(path: str, kuroco_handler: KurocoAPI, params: dict, limit: int = 10) -> KurocoResponse:
    """
    Send a query to the Kuroco API for embedding

    Parameters:
    path (str): The path to the Kuroco API
    kuroco_handler (KurocoAPI): The KurocoAPI object used for Kuroco API requests
    params (dict): The parameters to be sent with the get request
    limit (int): The maximum number of entries to return, 0 for all

    Returns:
    list: A list of embedded entries similar to the query

    Note:
    This method is asynchronous. 
    """
    query = prepare_request(path=path, params=params, limit=limit)
    query.pop("data", None)
    k_response = await kuroco_handler.get(**query)
    return k_response


def check_topics_ids(min_length: int = 1):
    """
    Decorator that checks that topics_ids is a list of integers with minimum length
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            topics_ids = kwargs.get("topics_ids", [])
            assert isinstance(topics_ids, list), "Topics_ids must be a list"
            assert len(topics_ids) >= min_length, f"Topics_ids must be a list of integers with minimum length {min_length}"
            assert all(isinstance(x, int) for x in topics_ids), "Topics_ids must be a list of integers"
            return await func(*args, **kwargs)
        return wrapper
    return decorator
