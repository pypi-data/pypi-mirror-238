import asyncio
from .kuroco_api import KurocoAPI
import pandas as pd
from pandas import DataFrame
from uuid import uuid4

NAME_OF_CATEGORY = uuid4().hex

class KurocoContent():
    _kuroco_handler = None
    _title: str = None
    _path: str = None
    _description: str = None
    _topics: dict = None
    _operations_endpoints: dict = {'list': NAME_OF_CATEGORY, 'insert': NAME_OF_CATEGORY, 'update': NAME_OF_CATEGORY, 'delete': f'{NAME_OF_CATEGORY}-deletes'}

    def __init__(self, title: str, path: str, kuroco_api: KurocoAPI = None, operations_endpoints: dict = {}) -> None:
        self._title = title
        self.kuroco_handler = KurocoAPI() if kuroco_api is None else kuroco_api
        self.path = path
        self._operations_endpoints = {**self._operations_endpoints, **operations_endpoints}

    @property
    def kuroco_handler(self):
        return self._kuroco_handler
    
    @kuroco_handler.setter
    def kuroco_handler(self, value):
        assert isinstance(value, KurocoAPI), f"Kuroco handler must be a KurocoAPI instance, not {type(value)}"
        self._kuroco_handler = value

    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        assert isinstance(value, str), f"Title must be a string, not {type(value)}"
        self._title = value

    @property
    def path(self):
        return self._path
    
    @path.setter
    def path(self, value):
        assert isinstance(value, str), f"Path must be a string, not {type(value)}"
        self._path = value

    def get_template(self):
        ret = dict.fromkeys(self.schema)
        # Remplace the None values with empty strings
        for key in ret:
            if ret[key] is None:
                ret[key] = ""        
        return ret

    async def refresh(self):
        """
        Refresh the category

        Parameters:
        None

        Returns:
        DataFrame: The topics in the category
        """
        self._topics = await self.list()

    def get_operation_endpoint(self, operation: str):
        """
        Get the endpoint of an operation

        Parameters:
        operation (str): The operation to get the endpoint from

        Returns:
        str: The endpoint of the operation
        """
        return self._operations_endpoints[operation].replace(NAME_OF_CATEGORY, self.path)

    def get_all_operations_endpoints(self):
        return {operation: self.get_operation_endpoint(operation) for operation in self._operations_endpoints}

    def __str__(self):
        return f"Category: {self.title}, path: {self.path}, description: {self.description}, topics: {self.topics_titles}, schema: {self.schema}, operations: {self.get_all_operations_endpoints()}"

    @property
    def topics(self):
        return self._topics
    
    @topics.setter
    def topics(self, _):
        raise AttributeError("Topics cannot be set directly, got at path changing time.")

    @property
    def name(self):
        return self._title

    @property  
    def schema(self):
        ret = list(self.topics.keys())
        ret.remove("topics_id")
        return tuple(ret)

    @property
    def description(self):
        return self._description

    @property
    def topics_titles(self):
        return tuple(self.topics.keys())

    @property
    def topics_ids(self):
        return tuple(self.topics["topics_id"])

    @property
    def topics_count(self):
        return len(self.topics)
    
    @property
    def dtypes(self):
        return self.topics.dtypes

    async def get_content(self, topic_id: int):
        """
        Get the content of a topic in the category

        Parameters:
        topic_id (int): The id of the topic to get the content from

        Returns:
        dict: The content of the topic

        Examples:
        >>> category = KurocoCategory("test", "test", {"test": 1}, {})
        >>> await category.get_content(1)

        Note:
        The topic id must be in the category topics
        """
        assert topic_id in self.topics, f"Topic id {topic_id} not found in category {self._title}"
        result = self._kuroco_handler.get(self._operations_endpoints["list"], {"filter": f"topics_id = {topic_id}"})
        return result

    async def list(self):
        """
        List the topics in the category

        Parameters:
        None

        Returns:
        DataFrame: The topics in the category

        Examples:
        >>> category = KurocoCategory("test", "test", {"test": 1}, {"list": "list"})    
        >>> await category.list()
        """
        h_code, results = await self._kuroco_handler.get(self.get_operation_endpoint('list'), {})
        return DataFrame(results['list'])

    def convert_types_to_category(self, content: dict):
        """
        Convert the types of the content to the category types

        Parameters:
        content (dict): The content to be converted

        Returns:
        dict: The converted content
        """
        to_remove: list = []
        for key in content:
            if content[key] is None or content[key] == "":
                to_remove.append(key)
                continue
            if self.dtypes[key] == "int64":
                content[key] = int(content[key])
            elif self.dtypes[key] == "float64":
                content[key] = float(content[key])
            elif self.dtypes[key] == "bool":
                content[key] = bool(content[key])
        return {key: content[key] for key in content if key not in to_remove}

    async def insert(self, content: dict):
        """
        Insert a new topic in the category
        
        Parameters:
        content (dict): The content to be inserted
        
        Returns:
        dict: The results of the insertion
        
        Examples:
        >>> category = KurocoCategory("test", "test", {"test": 1}, {"insert": "insert"})
        >>> await category.insert({"test": "test"})

        Note:
        The content must be a dictionary with the same keys as the category schema
        """
        assert isinstance(content, dict), f"Content must be a dictionary, not {type(content)}"
        assert set(content.keys()) == set(self.schema), f"Content keys must be the same as the category schema, got {set(content.keys())} instead of {set(self.schema)}"
        content = self.convert_types_to_category(content)
        h_code, results = await self._kuroco_handler.post(self.get_operation_endpoint("insert"), data={**content, **{"open_flg": 1}})
        if h_code == 201:
            df_temp = DataFrame(content, index=[0])
            df_temp["topics_id"] = results["id"]
            self._topics = pd.concat([self._topics, df_temp], ignore_index=True)
        return results

    async def update(self, topics_id: int, content: dict):
        """
        Update a topic in the category

        Parameters:
        topics_id (int): The id of the topic to be updated
        content (dict): The content to be updated

        Returns:
        dict: The results of the update

        Examples:
        >>> category = KurocoCategory("test", "test", {"test": 1}, {"update": "update"})
        >>> await category.update(1, {"test": "test"})

        Note:
        The content must be a dictionary with the same keys as the category schema
        """
        assert isinstance(content, dict), f"Content must be a dictionary, not {type(content)}"
        assert set(content.keys()) <= set(self.schema), f"Content keys must be the same as the category schema, got {set(content.keys())} instead of {set(self.schema)}"
        content = self.convert_types_to_category(content)
        h_code, results = await self._kuroco_handler.put(self.get_operation_endpoint("update"), str(topics_id), data=content)
        if h_code == 200:
            self._topics.loc[self._topics["topics_id"] == topics_id, content.keys()] = content.values()
        return results

    async def delete(self, topics_ids):
        """
        Delete a topic in the category

        Parameters:
        topics_ids (int): The ids of the topics to be deleted

        Returns:
        dict: The results of the deletion

        Examples:
        >>> category = KurocoCategory("test", "test", {"test": 1}, {"delete": "delete"})
        >>> await category.delete(1)
        """
        if not isinstance(topics_ids, tuple | list):
            topics_ids = (topics_ids,)
        topics_ids = tuple(set(topics_ids))
        tasks = []
        assert all((topic_id in self.topics_ids for topic_id in topics_ids)), f"Topics ids must be in the category topics ids, got {topics_ids} instead of {self.topics_ids}"
        for topic_id in topics_ids:
            tasks.append(asyncio.create_task(self._kuroco_handler.delete(self.get_operation_endpoint("delete"), str(topic_id))))
        results = await asyncio.gather(*tasks)
        # Filter from topics_ids the topics that were not deleted
        topics_ids = [topic_id for topic_id, result in zip(topics_ids, results) if result[0] == 200]
        # Remove the deleted topics from the topics
        self._topics = self._topics[~self._topics["topics_id"].isin(topics_ids)]
        return results


class KurocoContentStructure:
    _kuroco_handler = None
    _content_structure_endpoint = "content_structure"

    _content_structure = {}
    def __init__(self, kuroco_api: KurocoAPI) -> None:
        self.content_structure = self._list()
        self.kuroco_handler = kuroco_api

    @property
    def content_structure(self):
        return self._content_structure
    
    @content_structure.setter
    def content_structure(self, value):
        assert isinstance(value, dict)
        self._content_structure = value

    def _list(self) -> None:
        """
        List the content structures 

        Parameters:
        None

        Returns:
        None
        """
        results = self._kuroco_handler.get_sync(self._content_structure_endpoint, {})
        return results

    async def get_content_category(self, category: str):
        """
        Get the content category from the content structure

        Parameters:
        category (str): The title of the category

        Returns:
        list: The category content
        """
        assert isinstance(category, str)
        assert category in self.content_structure
        results = await self._kuroco_handler.get(f"{self._content_structure_endpoint}/category/{category}",{}) 
        return results