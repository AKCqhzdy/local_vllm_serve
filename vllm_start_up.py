import subprocess
import time
import threading

MODEL_PATH = "/root/autodl-tmp/models/"

def run_vllm_serve(model_name="Llama3.1-1B", port=6008, gpu_fraction=0.9):
    """启动 vLLM 服务."""
    command = f"\
        vllm serve {MODEL_PATH}{model_name} \
        --disable-log-requests \
        --gpu-memory-utilization={gpu_fraction} \
        --max_model_len=1024 \
        --port={port} \
        --served-model-name {model_name}"
    print(f"运行命令: {command}")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:
        line = process.stdout.readline()
        if not line:
            break
        print(line.decode('utf-8').strip())

    # 等待进程结束
    process.wait()

    if process.returncode != 0:
        print(f"vLLM 服务启动失败，退出代码: {process.returncode}")
        print(process.stderr.read().decode('utf-8'))
        return False
    return True


if __name__ == "__main__":
    MODEL_NAMES = "Llama3.1-1B"
    if not run_vllm_serve(MODEL_NAMES):
        print("vLLM serve failed to start.")
        exit()
    time.sleep(10)
    print("All services started up successfully!")
    