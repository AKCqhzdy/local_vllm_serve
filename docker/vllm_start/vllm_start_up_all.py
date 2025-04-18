import subprocess
import time
import threading
import signal
import os

MODEL_PATH = "/root/autodl-tmp/models/"

def run_vllm_serve(model_name="Llama3.1-1B", port=6008, gpu_memory_utilization=0.9):
    """启动 vLLM 服务."""
    command = f"\
        vllm serve /root/autodl-tmp/models/{model_name} \
        --disable-log-requests \
        --gpu-memory-utilization={gpu_memory_utilization}\
        --max_model_len=1024 \
        --port={port} \
        --served-model-name {model_name}"
    print(f"运行命令: {command}")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:
        line = process.stdout.readline()
        if not line:
            break

        line_str = line.decode('utf-8').strip()
        print(line_str)
        if "Avg prompt throughput" in line_str:
            return process
        elif "ERROR" in line_str:
            print(f"vLLM service for {model_name} failed to start.")
            return None 
        elif process.poll() is not None:
            print(f"Process for {model_name} exited unexpectedly.  Return code: {process.returncode}")
            return None
    
    print(f"vLLM service for {model_name} finished without expected output.")
    return None

def run_vllm_serve_sequential(model_names):

    all_success = True
    process_list = []
    gpu_fraction = 0.9/len(model_names)
    for i, model_name in enumerate(model_names):
        port = 6008 + i
        process = run_vllm_serve(model_name, port, gpu_fraction*(i+1))
        if process:
            process_list.append(process)
            print(f"Started {model_name} successfully, port: {port}")
        else:
            print(f"Failed to start {model_name}")
            all_success = False

    return all_success, process_list


if __name__ == "__main__":
    MODEL_NAMES = ["Llama3.1-1B", "Qwen1.5-1.8B"]
    success, process_list = run_vllm_serve_sequential(MODEL_NAMES)
    if not success:
        print("at least one vLLM service failed to start.")
    else:
        print("All vLLM services started successfully.")
    
    for process in process_list:
        if process.poll() is None:
            print(f"Terminating process for {process.args}")
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                print(line.decode('utf-8').strip())    
            process.wait()

