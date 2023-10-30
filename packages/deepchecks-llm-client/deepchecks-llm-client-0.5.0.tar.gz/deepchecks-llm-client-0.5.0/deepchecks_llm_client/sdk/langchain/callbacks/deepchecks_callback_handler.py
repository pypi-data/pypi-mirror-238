import logging
import os
from collections import defaultdict
from datetime import datetime
from typing import Any, Union, Dict, List, Optional, Sequence
from uuid import UUID

from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import LLMResult
from langchain.schema.document import Document
from deepchecks_llm_client.client import DeepchecksLLMClient
from deepchecks_llm_client.data_types import Step, StepType, EnvType

from deepchecks_llm_client.client import DEFAULT_ENV_TYPE


class DeepchecksCallbackHandler(BaseCallbackHandler):
    """Base callback handler that can be used to handle callbacks from langchain."""

    def __init__(self, *args, app_name, app_version, env_type: EnvType = DEFAULT_ENV_TYPE,
                 host: str = None, api_key: str = None, logger: logging.Logger = None,
                 ext_interaction_id: Union[str, None] = None,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.api_key = api_key
        self.host = host
        self.app_name = app_name
        self.app_version = app_version
        self.env_type = env_type
        self.logger = logger or logging.getLogger(__name__)
        self._ext_interaction_id = ext_interaction_id
        self._user_input = None
        self._user_response = None
        self._steps: Dict[str, Step] = defaultdict()  # run_id -> Step

    @property
    def steps(self) -> List[Step]:
        return list(self._steps.values())

    @property
    def user_input(self) -> str:
        return self._user_input

    @property
    def user_response(self) -> str:
        return self._user_response

    @property
    def ext_interaction_id(self) -> Union[str, None]:
        return str(self._ext_interaction_id)

    def on_llm_start(
            self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> Any:
        """Run when LLM starts running."""
        self.logger.debug('on_llm_start', kwargs)
        run_id = kwargs['run_id']

        self._steps[str(run_id)] = Step(
            name="LLM",
            type=StepType.LLM,
            attributes=self.to_str_dict(kwargs),
            started_at=datetime.now().astimezone(),
            input='\n'.join(prompts),
        )

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        """Run when LLM ends running."""
        self.logger.debug('on_llm_end', kwargs)
        step = self._steps[str(kwargs['run_id'])]
        step.finished_at = datetime.now().astimezone()
        step.output = '\n'.join([a.json() for b in response.generations for a in b])

    def on_llm_error(
            self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> Any:
        """Run when LLM errors."""
        self.logger.debug('on_llm_error', kwargs)
        self._on_error(error, kwargs)

    def on_chain_start(
            self,
            serialized: Dict[str, Any],
            inputs: Dict[str, Any],
            *,
            run_id: UUID,
            parent_run_id: Optional[UUID] = None,
            tags: Optional[List[str]] = None,
            metadata: Optional[Dict[str, Any]] = None,
            **kwargs: Any,
    ) -> None:
        """Run when chain starts running."""
        if parent_run_id is None:
            self.logger.debug('on_chain_start', kwargs)
            self._user_input = inputs.get('input') or inputs.get('question') or inputs.get('text') or '\n'.join([str(v) for v in inputs.values()]) \
                if isinstance(inputs, dict) \
                else inputs

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> Any:
        """Run when chain ends running."""
        self.logger.debug('on_chain_end', kwargs)
        if kwargs.get('parent_run_id', None) is None:
            self._user_response = outputs.get('text') or outputs.get('output_text') or '\n'.join([str(v) for v in outputs.values()]) \
                if isinstance(outputs, dict) \
                else outputs

            self._log_interaction()

    def on_retriever_error(
            self,
            error: BaseException,
            *,
            run_id: UUID,
            parent_run_id: Optional[UUID] = None,
            **kwargs: Any,
    ) -> Any:
        """Run when Retriever errors."""
        self.logger.debug('on_retriever_error', kwargs)
        self._on_error(error, kwargs)

    def _on_error(self, error, kwargs):
        if step := self._steps.get(str(kwargs['run_id'])):
            step.finished_at = datetime.now().astimezone()
            step.error = str(error)
        self._log_interaction()

    def on_retriever_start(
            self,
            serialized: Dict[str, Any],
            query: str,
            *,
            run_id: UUID,
            parent_run_id: Optional[UUID] = None,
            tags: Optional[List[str]] = None,
            metadata: Optional[Dict[str, Any]] = None,
            **kwargs: Any,
    ) -> Any:
        """Run when Retriever starts running."""
        self.logger.debug('on_retriever_start', kwargs)
        self._steps[str(run_id)] = Step(
            name="Data Retriever",
            input=str(query),
            type=StepType.INFORMATION_RETRIVAL,
            attributes=self.to_str_dict(kwargs),
            started_at=datetime.now().astimezone(),

        )

    def on_retriever_end(
            self,
            documents: Sequence[Document],
            *,
            run_id: UUID,
            parent_run_id: Optional[UUID] = None,
            **kwargs: Any,
    ) -> Any:
        """Run when Retriever ends running."""
        self.logger.debug('on_retriever_end', kwargs)
        self._steps[str(run_id)].finished_at = datetime.now().astimezone()
        self._steps[str(run_id)].output = '\n'.join(d.page_content for d in documents)

    def _log_interaction(self):
        _client: DeepchecksLLMClient = DeepchecksLLMClient()
        _client.init(host=os.getenv('DEEPCHECKS_LLM_HOST', self.host),
                     api_token=os.getenv('DEEPCHECKS_LLM_API_KEY', self.api_key),
                     app_name=self.app_name,
                     version_name=self.app_version,
                     env_type=self.env_type,
                     auto_collect=False)
        result = _client.log_interaction(
            model_response=self.user_response,
            ext_interaction_id=self.ext_interaction_id,
            user_input=self.user_input,
            steps=self.steps,
            information_retrieval=None,
        )
        if not result:
            raise self.logger.error('Interaction logging failed')

    @staticmethod
    def to_str_dict(attributes):
        return {k: str(v) for k, v in attributes.items()}
