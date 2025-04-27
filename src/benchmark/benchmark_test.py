import asyncio
import json
import os
import sys
import time
import traceback
from dataclasses import dataclass, field
from typing import Optional, Union
import logging

import aiohttp
import huggingface_hub.constants
from tqdm.asyncio import tqdm
from transformers import (AutoTokenizer, PreTrainedTokenizer,
                          PreTrainedTokenizerFast)

# Configure logging (adjust level as needed)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


AIOHTTP_TIMEOUT = aiohttp.ClientTimeout(total=6 * 60 * 60)


class RequestFuncOutput:
    def __init__(self):
        self.success = False
        self.error = None
        self.generated_text = None
        self.ttft = None
        self.itl = []
        self.latency = None
        self.output_tokens = None
        
    def __repr__(self):
        return f"RequestFuncOutput(success={self.success}, \
        error={self.error}, \
        generated_text={self.generated_text}, \
        ttft={self.ttft}, \
        itl={self.itl}, \
        latency={self.latency}, \
        output_tokens={self.output_tokens})"


async def test_local_server(api_url, entry_point, model_name, prompt, expect_output_len):
    
    async with aiohttp.ClientSession(trust_env=True,
                                     timeout=AIOHTTP_TIMEOUT) as session:
        content = [{"type": "text", "text": prompt}]
        
        payload = {
            "entry_point": entry_point,
            "model": model_name,
            "messages": [
                {
                    "role": "user",
                    "content": content
                },
            ],
            "max_completion_tokens": expect_output_len,
            "stream": True,
            "stream_options": {
                "include_usage": True,
            },
            "n": 1,
            "seed": 1,
            "top_p": 1,
            "top_k": 1,
            "temperature": 1,
            "repetition_penalty": 1,
            "logprobs": False,
            "echo": True,
            "min_p": 0.95,
            "presence_penalty": 1,
            "frequency_penalty": 1,
        }
        headers = {
            "Content-Type": "application/json",
            "Model-Name": model_name,
            "Entry-Point": entry_point
        }

        output = RequestFuncOutput()
        logging.info("Sending payload to server:")
        logging.info(payload)

        generated_text = ""
        ttft = 0.0
        st = time.perf_counter()
        most_recent_timestamp = st
        try:
            async with session.post(url=api_url, json=payload,
                                    headers=headers) as response:
                if response.status == 200:
                    async for chunk_bytes in response.content:
                        # print(chunk)
                        chunk_bytes = chunk_bytes.strip()
                        if not chunk_bytes:
                            continue

                        chunk = chunk_bytes.decode("utf-8").removeprefix(
                            "data: ")
                        if chunk != "[DONE]":
                            timestamp = time.perf_counter()
                            data = json.loads(chunk)
                            if choices := data.get("choices"):
                                content = choices[0]["delta"].get("content")
                                # First token
                                if ttft == 0.0:
                                    ttft = timestamp - st
                                    output.ttft = ttft

                                # Decoding phase
                                else:
                                    output.itl.append(timestamp -
                                                      most_recent_timestamp)

                                generated_text += content or ""
                            elif usage := data.get("usage"):
                                output.output_tokens = usage.get(
                                    "completion_tokens")

                            most_recent_timestamp = timestamp

                    output.generated_text = generated_text
                    output.success = True
                    output.latency = most_recent_timestamp - st
                else:
                    try:
                        error_text = await response.text()
                        output.error = f"HTTP {response.status}: {error_text}"
                    except Exception as e:
                        output.error = f"HTTP {response.status}: Error reading response body: {e}"
                    output.success = False
        except Exception:
            output.success = False
            exc_info = sys.exc_info()
            output.error = "".join(traceback.format_exception(*exc_info))
            logging.error(f"An exception occurred: {output.error}")  # Log the full traceback

    return output
    

async def main():
    
    tasks: list[asyncio.Task] = []
    tasks.append(
        asyncio.create_task(
            test_local_server(
                api_url = "http://127.0.0.1:6006",
                entry_point = "/v1/chat/completions",
                # model_name = "Llama-3.1-8B-Instruct",
                model_name="Llama3.1-1B",
                prompt = "print abcde....",
                expect_output_len = 100,
            )
        )
    )
    results = await asyncio.gather(*tasks)
    logging.info("results:")
    logging.info(results[0])

if __name__ == "__main__":

    asyncio.run(main())