import os

from typing import List, Tuple, Union, Dict


from kuroco_api import KurocoAPI, KurocoContent

from .kuroco_retriever import KurocoRetriever

from .CONFIG import QUERY_KW, SCORE_DISTANCE_COLUMN_NAME
from .tools import send_queries

class KurocoEmbedding:
    """
    A class used to represent a KurocoEmbedding object

    Attributes:
    _kuroco_handler (KurocoAPI): The KurocoAPI object used for Kuroco API requests
    _content (KurocoContent): The KurocoContent object used for embedding requests

    Examples:
    >>> # Embedding Instantiated on a single endpoint

    >>> k_emb = KurocoEmbedding(content="test", kuroco_handler= KurocoAPI())

    >>> k_emb.similarity_search("test query")
    """
    _kuroco_embedding_endpoint: str
    _kuroco_handler: KurocoAPI
    _content: List[KurocoContent]

    def __init__(self, 
                content: Union[Tuple[str], List[str], str],
                kuroco_handler: Union[KurocoAPI, 
                                    str, 
                                    None, 
                                    Tuple[str, str, Union[str, int]], 
                                    Dict[str, Union[str, int]]] = None,) -> None:  
        self.kuroco_handler = kuroco_handler
        self.content = content

    @property
    def content(self):
        return self._content
    
    @content.setter
    def content(self, value : Union[Tuple[str], List[str], str]):
        if isinstance(value, str):
            value = (value,)
        assert isinstance(value, (tuple, list)), "Content must be a list or a tuple (of strings) or a single string"
        if isinstance(value, (list, tuple)):
            assert all(isinstance(x, str) for x in value), "Content must be a list or a tuple of strings"
        assert len(set(value)) == len(value), "Content must be a list of unique strings"
        self._content = [KurocoContent(x, x, self.kuroco_handler) for x in value]

    @property
    def kuroco_handler(self):
        return self._kuroco_handler
    
    @kuroco_handler.setter
    def kuroco_handler(self, value: Union[KurocoAPI, 
                                          str, 
                                          Tuple, 
                                          List, 
                                          Dict[str, Union[str, int]], None]):
        if isinstance(value, KurocoAPI):
            pass
        elif isinstance(value, str):
            value = KurocoAPI.load_from_file(path=value)
        elif value is None:
            value = KurocoAPI()
        elif isinstance(value, (tuple, list)):
            value = KurocoAPI(*value)
        elif isinstance(value, dict):
            value = KurocoAPI(**value)
        else:
            raise AssertionError("KurocoAPI object must be provided as an argument (str, tuple or list) or as an environment variable")
        self._kuroco_handler = value

    def as_retriever(self, relevant: Union[str, List[str], Tuple[str]] = "subject", threshold: float = 0.8, limit: Union[int, None] = None):
        return KurocoRetriever(self, relevant=relevant, threshold=threshold, limit=limit)

    def as_vector_store(self, columns_vector: List[str]):
        #TODO
        return False
        #return KurocoVectorStore(self, column_vector=column_vector)

    @property
    def paths(self):
        return [content.path for content in self.content]
    
    # Methods for indirect query search
    async def similarity_search(self, query: str, limit: int = 10, filter: dict = {}, with_score: bool = False, threshold: float = 0.0):
        """
        Search for similar entries to a query

        Parameters:
        query (str): The query to search for similar entries to
        limit (int): The maximum number of entries to return, 0 for all
        filter (str): The filter to apply to the query
        with_score (bool): Whether to return the similarity score or not
        threshold (float): The similarity threshold to apply to the query

        Returns:
        dataframe: A dataframe of similar entries to the query, with their similarity score as last column if needed and limited to limit passed as parameter and by respecting the threshold provided

        Note:
        This method is asynchronous.

        TODO: Implement Document search
        """
        values = await self.similarity_search_by_query(query=query,
                                                       limit=limit,
                                                       filter=filter,
                                                       threshold=threshold) if not with_score else await self.similarity_search_by_query_with_score(query=query, 
                                                                                                                                                    limit=limit, 
                                                                                                                                                    filter=filter, 
                                                                                                                                                    threshold=threshold)
        return values

    async def similarity_search_by_query(self, query: str, limit: int = 10, filter: dict = {}, threshold: float = 0.0):
        """
        Search for similar entries to a query

        Parameters:
        query (str): The query to search for similar entries to
        limit (int): The maximum number of entries to return, 0 for all
        filter (dict): The filter to apply to the query
        threshold (float): The similarity threshold to apply to the query

        Returns:
        dataframe: A dataframe of similar entries to the query

        Note:
        This method is asynchronous.
        """
        # Cleaning the chain of characters
        query = query.strip().encode('utf-8', 'ignore').decode('utf-8')
        params = { QUERY_KW: query, "filter": filter }
        return (await send_queries(paths=self.paths, 
                                   kuroco_handler=self.kuroco_handler, 
                                   params=params, 
                                   limit=limit, 
                                   threshold=threshold)).drop(columns=[SCORE_DISTANCE_COLUMN_NAME], errors='ignore')

    async def similarity_search_by_query_with_score(self, query: str, limit: int = 10, filter: dict = {}, threshold: float = 0.0):
        """
        Search for similar entries to a query and return the similarity score

        Parameters:
        query (str): The query to search for similar entries to
        limit (int): The maximum number of entries to return, 0 for all
        filter (dict): The filter to apply to the query
        threshold (float): The similarity threshold to apply to the query

        Returns:
        dataframe: A dataframe of similar entries to the query with their similarity score for last column

        Note:
        This method is asynchronous.
        """
        params = { QUERY_KW: query, "filter": filter }
        return await send_queries(paths=self.paths, 
                                  kuroco_handler=self.kuroco_handler,
                                  params=params, 
                                  limit=limit, 
                                  threshold=threshold)

    async def similarity_search_with_score(self, query: str, limit: int = 10, threshold: float = 0.0):
        """
        Search for similar entries to a query and return the similarity score

        Parameters:
        query (str): The query to search for similar entries to
        limit (int): The maximum number of entries to return, 0 for all

        Returns:
        dataframe: A dataframe of similar entries to the query with their similarity score for last column 
        
        Note:
        This method is asynchronous. Use similarity_search_with_score_sync for a synchronous version
        """
        return await self.similarity_search_by_query_with_score(query, limit, threshold)
    
    async def fetch_vectors(self, ids: list):
        # TODO
        return False