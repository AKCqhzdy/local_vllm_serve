## Quick Start 

```bash
# Run on proj54
cp .env.example .env
# Change the environment variables in the .env file to your own, especially the `HUGGING_FACE_HUB_TOKEN`

# Run the script to start the containers
chmod +x docker/run_proj54.sh
./docker/run_proj54.sh

# Send test request
python src/create_payload.py
```

## Configuration

### vLLM
#### Description
`docker/Dockerfile.base` is the base image for vLLM with some common packages installed. Besides, `docker/prepare_model.sh` is a script that prepares the model for vLLM. It creates a ``conf.toml`` file in the model directory and downloads the model from the HuggingFace Hub. This script will be called when you run `docker-compose up` in `docker/docker-compose.yml`. We use .env file to pass the environment variables to the container. Please change the environment variables in the .env file to your own. For quick start, you can only change the `HUGGING_FACE_HUB_TOKEN` in the to your own.
#### Network configuration
If you want to run the vLLM on your own machine, you can change the `docker/docker-compose.yml` file to run the vLLM on your own machine. For example, the `docker/docker-compose_proj54.yml` and `docker/Dockerfile.proj54.base` are the configuration for running the vLLM on our own server.

### Nignx reverse proxy

Move ``proxy.conf`` from your project to niginx configuration directory（/etc/niginx/con.d）. This way nginx will listen to port 6006 and forward to 6008 and 6009 depending on the selected model. Do remember to add the config for the new added model config to the ``proxy.conf`` file.


### Send request

Usage: python ``src/send_request.py`` <api_url> <payload_json>

For a quick start, you can modify the payload directly in ``src/create_payload.py`` and then run that script. 

```bash
python src/create_payload.py
```

Response(openai format) will be displayed

### Benchmark

We also provide a benchmark script to test the performance of the vLLM. The benchmark script is in `benchmark/benchmark.py`. You can run the benchmark script by `python benchmark/benchmark.py`.