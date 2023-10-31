import asyncio

from dataclasses import dataclass
from typing import List, Union, Tuple
from pydantic import Extra
from langchain.schema.retriever import BaseRetriever
from langchain.schema.document import Document
from langchain.docstore.document import Document

THRESHOLD = 0.8
@dataclass
class KurocoRetriever (BaseRetriever, extra=Extra.allow):
    """
    KurcoRetriever is a retriever that uses KurocoEmbedding to search for similar documents.
    It is designed to be used in Langchain.

    It requires a KurocoEmbedding instance and a list of relevant columns to search for.

    Extra Attributes:
        _embedder (KurocoEmbedding): The KurocoEmbedding object used for embedding requests
        _relevant (list): The list of relevant columns to search for
        _limit (int): The maximum number of results to return

    Examples:
        >>> from kuroco import KurocoAPI, KurocoEmbedding
        >>> k_api = KurocoAPI.load_from_file(path='kuroco.json')
        >>> k_emb = KurocoEmbedding(('Shops', 'Zones'), k_api)
        >>> k_retriever = KurocoRetriever(k_emb, 'subject')
        >>> def format_docs(docs):
        >>>     return "\n\n".join([d.page_content for d in docs])
        >>> chain = (
        >>>     {"context": k_retriever | format_docs, "question": RunnablePassthrough()}
        >>>     | prompt
        >>>     | model
        >>>     | StrOutputParser()
        >>> )
        >>> chain.invoke("query")

    """
    _embedder: 'KurocoEmbedding'
    _relevant: list
    _threshold: float
    _limit: Union[int, None]

    def __init__(self, 
                 k_emb: 'KurocoEmbedding', 
                 relevant: Union[List[str], Tuple[str], str], 
                 threshold: float = THRESHOLD, 
                 limit: Union[int, None] = None):
        BaseRetriever.__init__(self)

        self.embedder = k_emb

        assert isinstance(relevant, (list, tuple, str)), "Relevant must be a list, tuple or string"
        self.relevant = relevant
        
        assert isinstance(threshold, float) and 0 <= threshold <= 1, "Threshold must be a float between 0 and 1"
        self.threshold = threshold

        assert isinstance(limit, int) or limit is None, "Limit must be an integer or None"
        self.limit = limit
    
    def _get_relevant_documents(
        self, query: str, *, run_manager 
    ) -> List[Document]:
        """
        Returns a list of `Document` objects that are relevant to the given `query`.
        The relevance is determined by a similarity search performed by the `embedder`
        object stored in the `metadata` dictionary. The search is limited to `limit`
        results and a `threshold` score. Only the columns specified in the `relevant`
        list of the `metadata` dictionary are considered for the search. The resulting
        `Document` objects have their `page_content` set to the relevant text and their
        `metadata` set to a dictionary containing the source of the document (`kuroco`)
        and the name of the relevant column.
        
        Args:
            query (str): The query string to search for.
            run_manager: A run manager object.
            
        Returns:
            List[Document]: A list of `Document` objects that are relevant to the query.
        """
        loop = asyncio.new_event_loop()
        results = loop.run_until_complete(self.embedder.similarity_search(query, limit=self.limit, with_score=False, threshold=self.threshold))
        loop.close()

        # If no relevant column is asked, then transform all the dataframe into a list of documents
        selected_columns = [col for col in self.relevant if col in results.columns] if self.relevant else results.columns
        return [Document(page_content=w, 
                         metadata={"source": "kuroco", 
                                    "field": selected_columns[i]})
                        for v in results.loc[:, selected_columns].values.tolist()
                        for i, w in enumerate(v) if w
                ]
    