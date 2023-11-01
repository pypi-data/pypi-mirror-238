# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Utilities for importing required dependencies."""
from azureml.metrics.common.exceptions import MissingDependencies, ValidationException


def load_sklearn():
    try:
        import sklearn
        import sklearn.metrics
    except ImportError:
        safe_message = "Tabular packages are not available. " \
                       "Please run pip install azureml-metrics[tabular]"
        raise MissingDependencies(
            safe_message, safe_message=safe_message
        )
    return sklearn


def load_evaluate():
    try:
        import evaluate
    except ImportError:
        safe_message = "evaluate package is not available. Please run pip install azureml-metrics[evaluate]"
        raise MissingDependencies(
            safe_message, safe_message=safe_message
        )
    return evaluate


def load_openai_embeddings_utils():
    try:
        from openai.embeddings_utils import get_embedding
    except ImportError:
        safe_message = "openai.embedding_utils package is not available. Please run pip " \
                       "install azureml-metrics[ada-cosine-similarity]"
        raise MissingDependencies(
            safe_message, safe_message=safe_message
        )
    return get_embedding


def load_similarity_utils():
    try:
        from azureml.metrics.text.qa import _similarity_utils

    except ImportError:
        safe_message = "Relevant GPT Star metrics packages are not available. " \
                       "Please run pip install azureml-metrics[prompt-flow]"
        raise MissingDependencies(
            safe_message, safe_message=safe_message
        )
    return _similarity_utils


def load_rtoml():
    try:
        import rtoml
    except ImportError:
        safe_message = "Relevant RAG Evaluation packages are not available. " \
                       "Please run pip install azureml-metrics[rag-evaluation]"
        raise MissingDependencies(
            safe_message, safe_message=safe_message
        )
    return rtoml


def load_prompt_crafter():
    try:
        from azureml.metrics.common.templates.prompt_crafter import LLMPromptCrafter
    except ImportError:
        safe_message = "Relevant RAG Evaluation packages are not available. " \
                       "Please run pip install azureml-metrics[rag-evaluation]"
        raise MissingDependencies(
            safe_message, safe_message=safe_message
        )
    return LLMPromptCrafter


def load_rag_init_functions():
    try:
        from azureml.metrics.common.llm_connector._llm import setup_llm, is_chat_completion_api
    except ImportError:
        safe_message = "Relevant RAG Evaluation packages are not available. " \
                       "Please run pip install azureml-metrics[rag-evaluation]"
        raise MissingDependencies(
            safe_message, safe_message=safe_message
        )
    return setup_llm, is_chat_completion_api


def load_mmtrack_eval_mot():
    """Load mmtrack package for evaluation."""
    try:
        from mmtrack.core.evaluation.eval_mot import eval_mot
        return eval_mot
    except ImportError:
        msg = "mmtrack package import failed, the package is not installed. \
               mmtrack is in need in video multi-object-tracking scenario, \
               and it's going to be installed in azureml-acft-image-components. \
               please install mmtrack==0.14.0"
        return ValidationException(msg, safe_message=msg)
