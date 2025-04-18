## How to use

### use docker
start up docker-compose under the docker directory


### Start multiple vllm servers

environment: 

autoDL server

vllm 0.8.2

PyTorch 2.3.0

Python  3.12(ubuntu22.04)

CUDA  12.1



Make sure you have installed vllm.  autoDL image is recommended.

``vllm_start_up.py`` is provided to quickly start vllm serve on the server.  (Need to modify MODEL_PATH and MODEL_NAME) At present, each service needs to be started separately, and --gpu-memory-utilization need adjust



### Nignx reverse proxy

Make sure you have installed Nignx and start it by ``nignx``. 

Move ``proxy.conf`` from your project to niginx configuration directory（/etc/niginx/con.d）. This way nginx will listen to port 6006 and forward to 6008 and 6009 depending on the selected model. 



### Send request

Usage: python ``src/send_request.py`` <api_url> <payload_json>

For a quick start, you can modify the payload directly in ``src/create_payload.py`` and then run that script. 

```bash
python src/create_payload.py
```

Response(openai format) will be displayed
