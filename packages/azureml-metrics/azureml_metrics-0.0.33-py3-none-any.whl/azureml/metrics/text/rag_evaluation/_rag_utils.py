# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Utils for RAG Evaluation metrics."""
import importlib.resources
import logging
import time
from random import random
import functools
import traceback

from enum import Enum
from typing import Optional
from azureml.metrics.common.import_utilities import load_rtoml

logger = logging.getLogger(__name__)


class PromptDelimiter:
    conversation: str = "<Conversation>"
    endOfTokens: str = "<|im_end|>"
    startOfAnswer: str = "<Generated Answer>"
    documentationStart: str = "<DocumentationStart>"
    documentationEnd: str = "<DocumentationEnd>"
    documentation: str = "<Documentation>"
    docDelimiter: str = "<DOC>\n"
    promptStart: str = "<|im_start|>"
    promptEnd: str = "<|im_end|>"
    promptSeparator: str = "<|im_sep|>"
    promptSystem: str = "[system]"
    promptUser: str = "user"
    promptAssistant: str = "assistant"
    currentMessageIntent: str = "Current Message Intent"


class Speaker(Enum):
    USER = PromptDelimiter.promptUser
    BOT = PromptDelimiter.promptAssistant


def load_toml(prompt_file: str = "sbs_prompt.toml",
              source_module: Optional[str] = "azureml.metrics.text.rag_evaluation.prompt_templates") -> dict:
    # source_module: Optional[str] = "rag_evaluation.prompt_templates") -> dict:
    rtoml = load_rtoml()
    try:
        with importlib.resources.open_text(source_module, prompt_file, encoding="ISO-8859-1") as f:
            return rtoml.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"toml file loading error,double check this: {prompt_file}")


def get_prompt_prefix(filename: str,
                      version: str = "",
                      purpose: str = "retrieval",
                      keyword: str = "prefix"):
    """
    get prompt prefix

    :param filename: filename of the toml file
    :param version: version of the prompt - no version by default
    :param purpose: purpose of the prompt - "retrieval" or "generation"
    :param keyword: indicates if prefix to be used
    :return: prompt prefix and prompt template
    """
    prompt_dict = load_toml(filename)

    # use version control if there are more than one version of the prompt
    try:
        if version != "":
            prefix = prompt_dict[purpose][version][keyword] if keyword in prompt_dict[purpose][version] else ""
        else:
            prefix = prompt_dict[purpose][keyword] if keyword in prompt_dict[purpose] else ""
    except KeyError:
        raise KeyError(
            f"please check if keywords: {purpose}, prefix, examples(optional), {version} exist your toml file")
    prompt_prefix = prefix

    if prompt_prefix == "":
        raise ValueError(
            "prompt prefix is empty, we need the key word 'retrieval', 'prefix', 'examples(optional)' "
            "in the toml file")

    return prompt_prefix


def retry_with_exponential_backoff(max_retries: int = 50,
                                   delay_factor: float = 2.0,
                                   max_delay: float = 300.0,
                                   jitter: bool = True,
                                   verbose: bool = True):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries <= max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if retries == max_retries:
                        raise e

                    sleep_time = delay_factor ** retries
                    if jitter:
                        sleep_time = sleep_time * (0.5 + random())  # Add random jitter

                    sleep_time = min(sleep_time, max_delay)
                    if verbose:
                        logger.warning("Computation of RAG Evaluation metrics for {} failed with the following "
                                       "exception :\n {}".format(func, e))
                        logger.info("Traceback : \n {}".format(traceback.format_exc()))
                        logger.warning("Attempting retry "
                                       "number {} after {} seconds".format(retries,
                                                                           round(sleep_time, 2)))
                    time.sleep(sleep_time)
                    retries += 1
        return wrapper
    return decorator
