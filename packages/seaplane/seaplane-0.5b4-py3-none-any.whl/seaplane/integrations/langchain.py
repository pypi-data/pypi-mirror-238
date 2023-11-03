from typing import Any, List, Mapping, Optional

from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.embeddings.base import Embeddings
from langchain.llms.base import LLM
from langchain.vectorstores import Qdrant
from pydantic import BaseModel
import requests

from seaplane.config import config
from seaplane.sdk_internal_utils.http import headers
from seaplane.sdk_internal_utils.substation import SubstationAPI
from seaplane.sdk_internal_utils.token_auth import method_with_token
from seaplane.vector import vector_store


class SeaplaneEmbeddingFunction(BaseModel, Embeddings):
    @method_with_token
    def _embed(self, token: str, query: str) -> List[float]:
        url = config.substation_embed_endpoint

        resp = requests.post(
            url,
            headers=headers(token),
            json={"query": query},
        )
        resp.raise_for_status()
        result = resp.json()

        return [float(i) for i in result["embeddings"]]

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings = []
        for text in texts:
            response = self._embed(f"Represent the document for Retrieval: {text}")
            embeddings.append(response)
        return embeddings

    def embed_query(self, query: str) -> List[float]:
        response = self._embed(f"Represent the Science sentence: {query}")
        return response


seaplane_embeddings = SeaplaneEmbeddingFunction()


def langchain_vectorstore(index_name: str, embeddings: Embeddings = seaplane_embeddings) -> Qdrant:
    vectorstore = Qdrant(
        client=vector_store._get_client(),
        collection_name=index_name,
        embeddings=embeddings,
    )

    return vectorstore


class SeaplaneLLM(LLM):
    max_output_length: Optional[int] = 3000
    model_specific_prompt: Optional[bool] = True

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
        substation_api = SubstationAPI()
        result = substation_api.predict(prompt, self.max_output_length, self.model_specific_prompt)
        return str(result["choices"][0]["text"]["generated_text"])

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"model": "MPT-30B", "provider": "Seaplane"}
