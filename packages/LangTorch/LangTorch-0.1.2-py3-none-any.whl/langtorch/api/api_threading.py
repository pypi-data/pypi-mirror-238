import asyncio
import json
from typing import List
import logging
import time
from .openai_parallel_processor import process_api_requests_from_session
from .parallel_processor_utils import (
    api_endpoint_from_url,
    num_tokens_consumed_from_request,
    StatusTracker
)


async def execute_api_requests_in_parallel(
        session,
        request_type: str,
        job_id: str,
        request_url: str,
        api_key: str,
        max_requests_per_minute: float = 3_000 * 0.5,
        max_tokens_per_minute: float = 250_000 * 0.5,
        token_encoding_name: str = "cl100k_base",
        max_attempts: int = 3,
        logging_level: int = logging.ERROR,
):
    # run tasks in parallel
    await process_api_requests_from_session(
        session=session,
        request_type=request_type,
        job_id=job_id,
        request_url=request_url,
        api_key=api_key,
        max_requests_per_minute=float(max_requests_per_minute),
        max_tokens_per_minute=float(max_tokens_per_minute),
        token_encoding_name=token_encoding_name,
        max_attempts=int(max_attempts),
        logging_level=int(logging_level),
    )
