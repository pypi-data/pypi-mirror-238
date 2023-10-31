"""Wrapper around CSS vector database."""
from __future__ import annotations

import logging
import uuid
from abc import ABC
from typing import Any, Dict, Iterable, List, Optional, Tuple, Callable

from langchain.docstore.document import Document
from langchain.embeddings.base import Embeddings
from langchain.utils import get_from_env
from langchain.vectorstores.base import VectorStore

from pangukitsappdev.utils.time_date import now_millis

logger = logging.getLogger(__name__)


def _default_text_mapping(dim: int, metric: str = "inner_product") -> Dict:
    return {
        "mappings": {
            "properties": {
                "text": {"type": "text"},
                "vector": {
                    "type": "vector",
                    "dimension": dim,
                    "indexing": 'true',
                    "algorithm": "GRAPH",
                    "metric": metric
                },
            }
        }, "settings": {"index": {"vector": "true"}}}


def _default_script_query(query_vector: List[float],
                          metric: str = "inner_product") -> Dict:
    return {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": "vector_score",
                "lang": "vector",
                "params": {
                    "field": "vector",
                    "vector": query_vector,
                    "metric": metric
                }
            }
        }
    }


def _default_get_doc_with_score_func(hit: dict) -> Tuple[Document, float]:
    return (
        Document(
            page_content=hit["_source"]["text"],
            metadata=hit["_source"]["metadata"],
        ),
        hit["_score"],
    )


def _default_add_text_request(index_name: str,
                              vector: List[float],
                              content: str,
                              doc_metadata: dict) -> Tuple[str, dict]:
    es_id = str(uuid.uuid4())
    req = {
        "_op_type": "index",
        "_index": index_name,
        "vector": vector,
        "text": content,
        "metadata": doc_metadata,
        "_id": es_id,
    }

    return es_id, req


# CSSVectorSearch是抽象基类VectorStore的具体实现，它为所有矢量数据库实现定义了一个公共接口。
# 通过继承ABC类，弹性矢量搜索可以定义为抽象基类本身，允许创建具有自己特定实现的子类。
class CSSVectorSearch(VectorStore, ABC):
    """把CSS数据库包装成向量数据库，CSS是基于开源Elasticsearch开发的自研向量搜索数据库，连接不需要身份认证信息, 传入 URL 和 index 以及
    embedding 进行构造.

    示例:
        .. code-block:: python

            from langchain import ElasticVectorSearch
            from langchain.embeddings import OpenAIEmbeddings

            embedding = OpenAIEmbeddings()
            elastic_vector_search = ElasticVectorSearch(
                elasticsearch_url="http://localhost:9200",
                index_name="test_index",
                embedding=embedding
            )

    Args:
        elasticsearch_url (str): The URL for the Elasticsearch instance.
        index_name (str): The name of the Elasticsearch index for the embeddings.
        embedding (Embeddings): An object that provides the ability to embed text.
                It should be an instance of a class that subclasses the Embeddings
                abstract base class, such as OpenAIEmbeddings()

    Raises:
        ValueError: If the elasticsearch python package is not installed.
    """

    def __init__(
            self,
            elasticsearch_url: str,
            index_name: str,
            embedding: Embeddings,
            mapping_func: Callable[[int], Dict] = _default_text_mapping,
            script_query_func: Callable[[List[float]], dict] = _default_script_query,
            get_doc_with_score_func: Callable[[Dict], Tuple[Document, float]] = _default_get_doc_with_score_func,
            add_text_request_func: Callable[
                [str, List[float], str, dict], Tuple[str, dict]] = _default_add_text_request,
            **kwargs
    ):
        """
        初始化
        Args:
            elasticsearch_url: 作为elasticsearch.client.Elasticsearch的hosts参数，支持逗号分割的list
            index_name: 索引名称
            embedding: （Optional）embedding接口的实现类。如果不传递，则走文本检索的逻辑
            mapping_func: （Optional）支持传递自定义的构造mapping函数，允许自定义mapping。入参为向量字段的长度。返回索引的mapping
            script_query_func: （Optional）支持传递自定义的查询dsl构造方法，入参为待搜索的向量vector: List[float]。返回query dsl
            get_doc_with_score_func: (Optional)传递自定义的从检索结果获取（Document, score）数据的函数，入参是es的检索结果
            add_text_request_func: (Optional)传递自定义的函数，在批量添加索引数据时构造请求体。入参：索引名，向量，文档内容，文档元数据\n
                出参（文档id, 构造的请求体）
            **kwargs:
        """

        """Initialize with necessary components."""
        try:
            import elasticsearch
        except ImportError:
            raise ImportError(
                "Could not import elasticsearch python package. "
                "Please install it with `pip install elasticsearch`."
            )
        self.embedding = embedding
        self.index_name = index_name
        self.mapping_func = mapping_func
        self.script_query_func = script_query_func
        self.get_doc_with_score_func = get_doc_with_score_func
        self.add_text_request_func = add_text_request_func
        self.vector_fields = None

        try:
            from pangukitsappdev.vectorstores.proxy_http_requests import ProxyRequestsHttpConnection
            self.client = elasticsearch.Elasticsearch(elasticsearch_url, connection_class=ProxyRequestsHttpConnection,
                                                      **kwargs)
        except ValueError as e:
            raise ValueError(
                f"Your elasticsearch client string is mis-formatted. Got error: {e} "
            )

    def add_texts(
            self,
            texts: Iterable[str, dict],
            metadatas: Optional[List[dict]] = None,
            refresh_indices: bool = True,
            embeddings: List[List[float]] = None,
            **kwargs: Any,
    ) -> List[str]:
        """把文本embeddings后插入数据库.

        Args:
            texts: Iterable of strings to add to the vectorstore.
            metadatas: Optional list of metadatas associated with the texts.
            refresh_indices: (Optional)bool to refresh ElasticSearch indices, default True
            embeddings: (Optional) embeddings data, will call self.embedding.embed_documents if absent

        Returns:
            List of ids from adding the texts into the vectorstore.
        """
        batch_size = kwargs.get("batch_size", 100)
        # 一批一批的数据进行索引构建
        sub_texts = []
        sub_metadatas = []
        sub_embeddings = []

        embedding_func = self.embedding.embed_documents if self.embedding else None
        result = []
        for i, d in enumerate(texts):
            if (i + 1) % batch_size:
                sub_texts.append(d)
                if metadatas:
                    sub_metadatas.append(metadatas[i])
                if embeddings:
                    sub_embeddings.append(embeddings[i])
            else:
                if self.embedding:
                    a_result = self.add_texts_with_embeddings(sub_texts,
                                                              sub_embeddings if sub_embeddings else embedding_func(
                                                                  sub_texts, **kwargs),
                                                              sub_metadatas,
                                                              refresh_indices)
                else:
                    a_result = self.add_texts_without_embeddings(sub_texts, refresh_indices)
                result.extend(a_result)
                sub_texts = []
                sub_metadatas = []
                sub_embeddings = []
                logger.info(f"Indexed {i + 1} document")

        if sub_texts:
            if self.embedding:
                a_result = self.add_texts_with_embeddings(sub_texts,
                                                          sub_embeddings if sub_embeddings else embedding_func(
                                                              sub_texts, **kwargs),
                                                          sub_metadatas,
                                                          refresh_indices)
            else:
                a_result = self.add_texts_without_embeddings(sub_texts, refresh_indices)
            result.extend(a_result)

        return result

    def add_texts_with_embeddings(self, texts: List[str],
                                  embeddings: List[List[float]],
                                  metadatas=None,
                                  refresh_indices: bool = True):
        """
        使用已经embeddings好的数据进行插入
        Args:
            texts: 文本
            embeddings: 文本对应的embedding结果
            metadatas: 文本的元数据
            refresh_indices: 是否刷新索引

        Returns:

        """

        try:
            from elasticsearch.exceptions import NotFoundError
            from elasticsearch.helpers import bulk
        except ImportError:
            raise ImportError(
                "Could not import elasticsearch python package. "
                "Please install it with `pip install elasticsearch`."
            )
        dim = len(embeddings[0])
        # 定义索引映射
        mapping = self.mapping_func(dim)
        if not self.client.indices.exists(index=self.index_name):
            # 创建索引和映射
            self.client.indices.create(index=self.index_name,
                                       body=mapping)
            logger.info("Index created successfully.")
        bulk_requests = []
        ids = []
        for i, text in enumerate(texts):
            metadata = metadatas[i] if metadatas else {}
            _id, request = self.add_text_request_func(self.index_name, embeddings[i], text, metadata)
            ids.append(_id)
            bulk_requests.append(request)
        bulk(self.client, bulk_requests)
        if refresh_indices:
            self.client.indices.refresh(index=self.index_name)
        return ids

    def add_texts_without_embeddings(self, texts: List[str, dict], refresh_indices: bool = True):
        """
        CSS插件模式，使用原始文本数据进行插入
        Args:
            texts: 原始文本数据，支持多字段
            refresh_indices: 是否刷新索引

        Returns:

        """

        try:
            from elasticsearch.exceptions import NotFoundError
            from elasticsearch.helpers import bulk
        except ImportError:
            raise ImportError(
                "Could not import elasticsearch python package. "
                "Please install it with `pip install elasticsearch`."
            )

        if not self.client.indices.exists(index=self.index_name):
            # CSS插件模式索引需外部创建好
            raise ImportError(
                "index is not exists. Indexes should be created first."
            )
        bulk_requests = []
        ids = []
        for i, text in enumerate(texts):
            doc_metadata = {"text": text} if isinstance(text, str) else text

            # 请求体
            _id = str(uuid.uuid4())
            req = {
                "_index": self.index_name,
                "_id": _id,
            }
            req.update(doc_metadata)

            ids.append(_id)
            bulk_requests.append(req)
        bulk(self.client, bulk_requests)
        if refresh_indices:
            self.client.indices.refresh(index=self.index_name)
        return ids

    def similarity_search(
            self, query: str, k: int = 4, **kwargs: Any
    ) -> List[Document]:
        """返回和查询语句最相近的k条文本.

        Args:
            query: Text to look up documents similar to.
            k: Number of Documents to return. Defaults to 4.

        Returns:
            List of Documents most similar to the query.
        """
        docs_and_scores = self.similarity_search_with_score(query, k, **kwargs)
        documents = [d[0] for d in docs_and_scores]
        return documents

    def similarity_search_with_score(
            self, query: str, k: int = 4,
            score_threshold: float = 0.2,
            **kwargs: Any
    ) -> List[Tuple[Document, float]]:
        """Return docs most similar to query.
        Args:
            query: Text to look up documents similar to.
            k: Number of Documents to return. Defaults to 4.
            score_threshold: （Optional）低于这个阈值分数的doc不会被检索出来
        Returns:
            List of Documents most similar to the query.
        """

        if self.embedding:
            embedding = self.embedding.embed_query(query)
            return self.similarity_search_with_score_use_embedding_data(embedding, k, **kwargs)
        else:
            # 如果没有传递embedding，则执行如下逻辑
            return self._similarity_search_with_score_without_embedding(query=query,
                                                                        k=k,
                                                                        score_threshold=score_threshold,
                                                                        **kwargs)

    def similarity_search_with_score_use_embedding_data(self, embedding, k, **kwargs):
        response = self.client.search(index=self.index_name,
                                      body={'query': self.script_query_func(embedding)}, size=k, **kwargs)
        hits = [hit for hit in response["hits"]["hits"]]
        docs_and_scores = [
            self.get_doc_with_score_func(hit)
            for hit in hits
        ]
        return docs_and_scores

    def _similarity_search_with_score_without_embedding(self, query: str, k: int = 4,
                                                        include_fields: List[str] = None,
                                                        score_threshold: float = 0.8,
                                                        **kwargs: Any):
        """检索,不使用

        :param query: query词
        :param k: 检索结果数
        :param include_fields: (Optional)数据格式，检索出的结果包含哪些字段，默认["content"]
        :param min_score: (Optional) 只取大于等于min_score的检索结果
        :param get_document_with_score_func: (Optional)解析检索结果获得文档内容和对应的打分。默认调用default_get_document_with_score_func
        :param kwargs: 扩展参数
        :return: :class:`List[Document] <List[Document]>` 检索结果
        """

        # 从索引配置中读取向量字段
        self._get_css_vector_fields()
        query_dsl = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": include_fields if include_fields else self.vector_fields
                }
            },
            "from": 0,
            "size": k
        }

        start_millis = now_millis()
        rsp_json = self.client.search(index=self.index_name, body=query_dsl, size=k)
        end_millis = now_millis()

        duration_ms = end_millis - start_millis

        # 服务端处理的耗时信息
        server_cost_time = rsp_json.get("timestamp")
        # 服务端处理的状态
        server_status = rsp_json.get("status")

        logging.info(
            f"Success return, request cost: [duration_ms: {duration_ms}], [server_cost_time: {server_cost_time}], "
            f"[server_status: {server_status}]")

        # 解析搜索结果，支持从参数中传递解析函数
        docs_with_score: List[Tuple[Document, float]] = \
            [(
                Document(
                    page_content=h["_source"].get("content"),
                    metadata=h["_source"],
                ),
                h["_score"],
            ) for h in rsp_json["hits"]["hits"]]

        result = [dws for dws in docs_with_score if dws[1] >= score_threshold]

        return result

    def _get_css_vector_fields(self) -> None:
        """通过索引信息，获取向量数字段（CSS 插件模式）

        :return:
        """

        # 外部embedding模式，不需要读取；
        if self.vector_fields or self.embedding:
            return

        try:
            rsp_json = self.client.indices.get_settings(self.index_name)
            inference_field = rsp_json[self.index_name]["settings"]["index"]["inference"]["field"]
            self.vector_fields = list(map(lambda x: x.split(":")[0], inference_field))
        except IOError:
            logger.warning("get vector fields error.")

    def similarity_search_with_relevance_scores(self, query: str,
                                                k: int = 4, **kwargs: Any) -> List[Tuple[Document, float]]:
        return self.similarity_search_with_score(query, k, **kwargs)

    @classmethod
    def from_texts(
            cls,
            texts: List[str],
            embedding: Embeddings,
            metadatas: Optional[List[dict]] = None,
            elasticsearch_url: Optional[str] = None,
            index_name: Optional[str] = None,
            refresh_indices: bool = True,
            **kwargs: Any,
    ) -> CSSVectorSearch:
        """Construct ElasticVectorSearch wrapper from raw documents.

        This is a user-friendly interface that:
            1. Embeds documents.
            2. Creates a new index for the embeddings in the Elasticsearch instance.
            3. Adds the documents to the newly created Elasticsearch index.

        This is intended to be a quick way to get started.

        Example:
            .. code-block:: python

                from langchain import ElasticVectorSearch
                from langchain.embeddings import OpenAIEmbeddings
                embeddings = OpenAIEmbeddings()
                elastic_vector_search = ElasticVectorSearch.from_texts(
                    texts,
                    embeddings,
                    elasticsearch_url="http://localhost:9200"
                )
        """
        elasticsearch_url = elasticsearch_url or get_from_env(
            "elasticsearch_url", "ELASTICSEARCH_URL"
        )
        index_name = index_name or uuid.uuid4().hex
        vector_search = cls(elasticsearch_url, index_name, embedding, **kwargs)
        vector_search.add_texts(
            texts, metadatas=metadatas, refresh_indices=refresh_indices
        )
        return vector_search
