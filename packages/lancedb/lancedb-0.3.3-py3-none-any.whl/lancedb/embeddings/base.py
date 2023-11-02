import importlib
from abc import ABC, abstractmethod
from typing import List, Union

import numpy as np
import pyarrow as pa
from pydantic import BaseModel, Field, PrivateAttr

from .utils import TEXT


class EmbeddingFunction(BaseModel, ABC):
    """
    An ABC for embedding functions.

    All concrete embedding functions must implement the following:
    1. compute_query_embeddings() which takes a query and returns a list of embeddings
    2. get_source_embeddings() which returns a list of embeddings for the source column
    For text data, the two will be the same. For multi-modal data, the source column
    might be images and the vector column might be text.
    3. ndims method which returns the number of dimensions of the vector column
    """

    _ndims: int = PrivateAttr()

    @classmethod
    def create(cls, **kwargs):
        """
        Create an instance of the embedding function
        """
        return cls(**kwargs)

    @abstractmethod
    def compute_query_embeddings(self, *args, **kwargs) -> List[np.array]:
        """
        Compute the embeddings for a given user query
        """
        pass

    @abstractmethod
    def compute_source_embeddings(self, *args, **kwargs) -> List[np.array]:
        """
        Compute the embeddings for the source column in the database
        """
        pass

    def sanitize_input(self, texts: TEXT) -> Union[List[str], np.ndarray]:
        """
        Sanitize the input to the embedding function.
        """
        if isinstance(texts, str):
            texts = [texts]
        elif isinstance(texts, pa.Array):
            texts = texts.to_pylist()
        elif isinstance(texts, pa.ChunkedArray):
            texts = texts.combine_chunks().to_pylist()
        return texts

    @classmethod
    def safe_import(cls, module: str, mitigation=None):
        """
        Import the specified module. If the module is not installed,
        raise an ImportError with a helpful message.

        Parameters
        ----------
        module : str
            The name of the module to import
        mitigation : Optional[str]
            The package(s) to install to mitigate the error.
            If not provided then the module name will be used.
        """
        try:
            return importlib.import_module(module)
        except ImportError:
            raise ImportError(f"Please install {mitigation or module}")

    def safe_model_dump(self):
        from ..pydantic import PYDANTIC_VERSION

        if PYDANTIC_VERSION.major < 2:
            return dict(self)
        return self.model_dump()

    @abstractmethod
    def ndims(self):
        """
        Return the dimensions of the vector column
        """
        pass

    def SourceField(self, **kwargs):
        """
        Creates a pydantic Field that can automatically annotate
        the source column for this embedding function
        """
        return Field(json_schema_extra={"source_column_for": self}, **kwargs)

    def VectorField(self, **kwargs):
        """
        Creates a pydantic Field that can automatically annotate
        the target vector column for this embedding function
        """
        return Field(json_schema_extra={"vector_column_for": self}, **kwargs)


class EmbeddingFunctionConfig(BaseModel):
    """
    This model encapsulates the configuration for a embedding function
    in a lancedb table. It holds the embedding function, the source column,
    and the vector column
    """

    vector_column: str
    source_column: str
    function: EmbeddingFunction


class TextEmbeddingFunction(EmbeddingFunction):
    """
    A callable ABC for embedding functions that take text as input
    """

    def compute_query_embeddings(self, query: str, *args, **kwargs) -> List[np.array]:
        return self.compute_source_embeddings(query, *args, **kwargs)

    def compute_source_embeddings(self, texts: TEXT, *args, **kwargs) -> List[np.array]:
        texts = self.sanitize_input(texts)
        return self.generate_embeddings(texts)

    @abstractmethod
    def generate_embeddings(
        self, texts: Union[List[str], np.ndarray]
    ) -> List[np.array]:
        """
        Generate the embeddings for the given texts
        """
        pass
