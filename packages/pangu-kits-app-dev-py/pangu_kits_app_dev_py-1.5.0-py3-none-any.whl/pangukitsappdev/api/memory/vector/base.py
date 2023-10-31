#  Copyright (c) Huawei Technologies Co., Ltd. 2023-2023. All rights reserved.
import logging
from abc import ABC, abstractmethod
from typing import List, Any, Dict, Tuple, Union

from langchain.schema import Document as BaseDocument
try:
    from langchain.vectorstores import VectorStore
except ImportError:
    from langchain.schema.vectorstore import VectorStore
from pangukitsappdev.api.memory.vector.vector_config import VectorStoreConfig

logger = logging.getLogger(__name__)


class Document(BaseDocument):
    """继承langchain.schema.Document
    增加了打分字段
    Attributes:
        score: 文档的相似度打分
    """
    score: float = 0.0


class VectorApi(ABC):
    """Interface for vector store"""

    @abstractmethod
    def add_texts(self, texts: List[Union[str, dict]], metadatas: List[Dict[str, Any]] = None) -> List[str]:
        """写入文本
        Args:
            texts: 文本
            metadatas: (Optional) 扩展元数据，size和texts保持一致

        Returns:
            文档id列表lis

        """
        pass

    @abstractmethod
    def add_qa_texts(self, qa_texts: List[Dict[str, str]], weight: Dict[str, int]) -> List[str]:
        """写入QA文本
        Args:
            qa_texts: qa文本内容
            weight: 做embedding的比重，key值和qa_texts的元素保持一致

        Returns:
            文档id列表list
        """
        pass

    @abstractmethod
    def similarity_search(self, query: str, top_k: int = 4, score_threshold: float = 0.2) -> List[Document]:
        """相似性检索
        在向量库中检索和query相似的文档
        Args:
            query: 查询文本
            top_k: 返回不超过top_k的document，默认4
            score_threshold: 得分阈值，默认0.2

        Returns:
            一个Document list

        """
        pass

    @abstractmethod
    def clear(self):
        """删除索引"""
        pass


class AbstractVectorApi(VectorApi, ABC):
    """VectorApi接口的基类
    封装了一个langchain.vectorstores.VectorStore的实现类，用来适配VectorApi接口。
    子类需要实现create_vector_store，用来构造一个langchain.vectorstores.VectorStore的实现类
    Attributes:
        vector_config: VectorStoreConfig类型，封装了用来构造VectorStore的一些参数
        vector_store: langchain.vectorstores.VectorStore的实现类，通过create_vector_store方法构造
    """

    def __init__(self, vector_config: VectorStoreConfig):
        self.vector_config = vector_config
        self.vector_store: VectorStore = self.create_vector_store(vector_config)

    def add_texts(self, texts: List[Union[str, dict]], metadatas: List[Dict[str, Any]] = None) -> List[str]:
        batch_size = self.vector_config.bulk_size
        # 一批一批的数据进行索引构建
        sub_texts = []

        result = []
        for i, d in enumerate(texts):
            if (i + 1) % batch_size:
                sub_texts.append(d)
            else:
                a_result = self.vector_store.add_texts(texts, metadatas)
                result.extend(a_result)
                sub_texts = []
                logger.info(f"Indexed {i + 1} document")

        if sub_texts:
            a_result = self.vector_store.add_texts(texts, metadatas)
            result.extend(a_result)

        return result

    def add_qa_texts(self, qa_texts: List[Dict[str, str]], weight: Dict[str, int]) -> List[str]:
        raise NotImplementedError("Not implemented")

    def similarity_search(self, query: str, top_k: int = 4, score_threshold: float = 0.2, **kwargs) -> List[Document]:
        doc_with_score: List[Tuple[BaseDocument, float]] = \
            self.vector_store.similarity_search_with_relevance_scores(query=query, k=top_k,
                                                                      score_threshold=score_threshold,
                                                                      **kwargs)
        return [Document(page_content=ds[0].page_content, metadata=ds[0].metadata, score=ds[1])
                for ds in doc_with_score]

    def clear(self):
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def create_vector_store(self, vector_config: VectorStoreConfig) -> VectorStore:
        """使用VectorStoreConfig里的配置构造VectorStore实现类

        Args:
            vector_config: 相关配置

        Returns:
            实现类VectorStore接口的对象
        """
        pass
