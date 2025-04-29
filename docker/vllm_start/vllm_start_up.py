import subprocess
import time
import toml

def run_vllm_serve(model_name, port):
    """启动 vLLM 服务."""
    command = f"\
        vllm serve models/{model_name} \
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

    # 等待进程结束
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
        print("error: can not find conf.toml")
        exit(1)

    print(config)
    MODEL_NAME = config["model"].get("MODEL_NAME")
    PORT = config["model"].get("PORT")
    if not MODEL_NAME or not PORT:
        print("error: can not MODEL_NAME or PORT in config")
        exit(1)

    if not run_vllm_serve(MODEL_NAME,PORT):
        print("The vLLM service failed to start and the program exited")
        exit()
    time.sleep(10)
    print("start up success!")

