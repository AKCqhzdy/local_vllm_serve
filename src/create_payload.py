import json
import subprocess
import asyncio
import sys
import logging

# Configure logging (adjust level as needed)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_payload(entry_point, model_name, prompt, expect_output_len):
    """创建 payload 字典."""
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
    return payload



async def main():
    
    API_URL = "http://127.0.0.1:6006"
    ENTRY_POINT = "/v1/chat/completions"
    MODEL_NAME = "Llama3.1-1B"
    PROMPT = "print abcde...."
    EXPECT_OUTPUT_LEN = 100

    payload = create_payload(ENTRY_POINT, MODEL_NAME, PROMPT, EXPECT_OUTPUT_LEN)
    payload_json = json.dumps(payload)

    command = [
        "D:\pythonvenv\Scripts\python", #!!
        "send_request.py",
        API_URL,
        payload_json
    ]

    try:
        proc = await asyncio.create_subprocess_exec(
            *command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        while True:
            line = await proc.stdout.readline()
            if not line:
                break

            line = line.decode().strip()
            # logging.info(f"Received line: {line}") 
            if line:
                try:
                    data = json.loads(json.loads(line))

                    if "chunk" in data:
                        logging.info(data["chunk"])

                    elif "error" in data:
                        error_message = data["error"]
                        logging.error(f"Error from send_request.py: {error_message}")
                        break

                    else:
                        logging.warning(f"Unexpected data format: {data}")


                except json.JSONDecodeError as e:
                    logging.error(f"Error decoding JSON: {e}, Line: {line}")
                    break

        await proc.wait()
        if proc.returncode != 0:
            logging.error(f"send_request.py exited with code {proc.returncode}")

        stderr = await proc.stderr.read()
        if stderr:
            logging.error(f"send_request.py stderr:\n{stderr.decode()}")


    except FileNotFoundError:
        logging.error("Error: send_request.py not found. Make sure it's in the same directory or accessible in the PATH.")
    except Exception as e:
        logging.exception(f"An error occurred while running send_request.py: {e}")


if __name__ == "__main__":
    asyncio.run(main())