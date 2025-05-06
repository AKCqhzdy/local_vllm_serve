import subprocess
import time
import toml
import os

def run_vllm_serve(model_name, port):
    """Start vLLM."""
    command = f"\
        vllm serve /app/models/{model_name} \
        --disable-log-requests \
        --gpu-memory-utilization=0.9\
        --max_model_len=4096 \
        --port={port} \
        --served-model-name={model_name}"
    print(f"run command: {command}")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:
        line = process.stdout.readline()
        if not line:
            break
        print(line.decode('utf-8').strip())

    # Wait for the process to end
    process.wait()

    if process.returncode != 0:
        print(f"fail to start vLLM serve, exit code: {process.returncode}")
        print(process.stderr.read().decode('utf-8'))
        return False
    return True


if __name__ == "__main__":
    try:
        with open("conf.toml", "r") as f:
            config = toml.load(f)
    except FileNotFoundError:
        raise Exception(f"error: can not find in {os.path.abspath('conf.toml')}")

    print(config)
    MODEL_NAME = config["model"].get("MODEL_NAME")
    PORT = config["model"].get("PORT")
    if not MODEL_NAME or not PORT:
        raise Exception("error: can not find MODEL_NAME or PORT in config")

    if not run_vllm_serve(MODEL_NAME,PORT):
        raise Exception("The vLLM service failed to start and the program exited")

    time.sleep(10)
    print("start up success!")

