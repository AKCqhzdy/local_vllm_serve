import asyncio
import json
import sys
import time
import traceback

import aiohttp


AIOHTTP_TIMEOUT = aiohttp.ClientTimeout(total=6 * 60 * 60)

async def send_request(api_url, payload_json):

    try:
        payload = json.loads(payload_json)
    except json.JSONDecodeError as e:
        yield json.dumps({"error": str(e)})
        return ;
    
    async with aiohttp.ClientSession(trust_env=True, timeout=AIOHTTP_TIMEOUT) as session:

        headers = {
            "Content-Type": "application/json",
            "Model-Name": payload.get("model"),
            "Entry-Point": payload.get("entry_point")
        }

        generated_text = ""
        st = time.perf_counter()

        try:
            async with session.post(url=api_url, json=payload, headers=headers) as response:
                if response.status == 200:
                    async for chunk_bytes in response.content:
                        chunk_bytes = chunk_bytes.strip()
                        if not chunk_bytes:
                            continue

                        chunk = chunk_bytes.decode("utf-8")
                        yield json.dumps({"chunk": chunk}) 
                else:
                    try:
                        error_text = await response.text()
                        yield json.dumps({"error": f"HTTP {response.status}: {error_text}"})
                    except Exception as e:
                        yield json.dumps({"error": f"HTTP {response.status}: Error reading response body: {e}"})
        except Exception:
            exc_info = sys.exc_info()
            error_message = "".join(traceback.format_exception(*exc_info))
            yield json.dumps({"error": error_message})

async def main(api_url, payload_json):
    try:
        async for item in send_request(api_url, payload_json):
            print(json.dumps(item))

    except json.JSONDecodeError as e:
        print(json.dumps({"error": str(e)}))
    except Exception as e:
        print(json.dumps({"error": str(e)}))

if __name__ == "__main__":
    
    if len(sys.argv) != 3:
        print("Usage: python send_request.py <api_url> <payload_json>")
        sys.exit(1)

    api_url = sys.argv[1]
    payload_json = sys.argv[2]

    asyncio.run(main(api_url, payload_json))