# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import pandas as pd

from typing import Any, Dict, Optional, List
from dataclasses import dataclass, field

from azureml.metrics.common.exceptions import OAIClientContentFilterException


class LLMState:
    """Maintain the state of LLM usage"""

    def __init__(self):
        self.total_token_usage = 0
        self.prompt_token_usage = 0
        self.completion_token = 0

    def update(self, total_token_usage=0, prompt_token_usage=0, completion_token=0):
        self.total_token_usage += total_token_usage
        self.prompt_token_usage += prompt_token_usage
        self.completion_token += completion_token

    def __str__(self):
        return f"LLMState(total_token_usage={self.total_token_usage}, " \
               f"prompt_token_usage={self.prompt_token_usage}, completion_token={self.completion_token})"

    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise KeyError(f'Invalid key: {key}')


@dataclass
class OAIGenerationConfig:
    """Class to hold OAI config. Used to instantiate GPTEndpoint

    Members:
        model: str - model to use for chatbot
        temperature: float - temperature to use for chatbot
        top_p: float - top_p to use for chatbot
        max_tokens: int - max_tokens to use for chatbot
        stop: Optional[List[str]] - stop to use for chatbot
    """
    # TODO: check if we need to use different default model
    model: str = "chatgpt"
    temperature: float = 0.0
    top_p: float = 1.0
    max_tokens: int = 1000
    stop: Optional[List[str]] = field(default_factory=list)
    is_streaming: bool = False


def handle_finish_reason(response: Dict[str, Any], llm_state: Optional[LLMState]) -> Optional[str]:
    if 'finish_reason' not in response["choices"][0]:
        return None
    finish_reason = response["choices"][0]['finish_reason']
    if not finish_reason:
        return None
    if finish_reason == 'content_filter':
        raise OAIClientContentFilterException()
    # calculate tokens if not a content filter error and llm state is available
    if 'usage' in response:
        usage = response['usage']
        if usage and 'total_tokens' in usage and llm_state:
            llm_state.update(
                total_token_usage=usage['total_tokens'],
                prompt_token_usage=usage['prompt_tokens'],
                completion_token=usage['completion_tokens']
            )
    if finish_reason == 'length':
        # TODO: check if we need to return an exception here
        return 'stop'  # raise LengthFinishException()
    elif finish_reason == 'stop':
        return 'stop'


def conversation_metric_aggregation(report_df: pd.DataFrame):
    conversation_avg_scores = report_df.mean().round(2)
    return conversation_avg_scores
