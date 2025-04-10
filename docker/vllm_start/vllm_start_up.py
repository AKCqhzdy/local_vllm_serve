import subprocess
import time
import toml

def run_vllm_serve(model_name="Llama3.1-1B", port=6008):
    """启动 vLLM 服务."""
    command = f"\
        vllm serve models/{model_name} \
        --disable-log-requests \
        --gpu-memory-utilization=0.9\
        --max_model_len=1024 \
        --port={port} \
        --served-model-name {model_name}\
        --disable-async-output-proc\
        --device=cpu "
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
    
    try:
        with open("conf.toml", "r") as f:
            config = toml.load(f)
    except FileNotFoundError:
        print("错误: 找不到 conf.toml 文件")
        exit(1)

    print(config) 
    MODEL_NAME = config["model"].get("MODEL_NAME")
    PORT = config["model"].get("PORT")
    if not MODEL_NAME or not PORT:
        print("错误: 配置文件中缺少 MODEL_NAME 或 PORT")
        exit(1)
        
    if not run_vllm_serve(MODEL_NAME,PORT):
        print("vLLM 服务启动失败，程序退出")
        exit()
    time.sleep(10)
    print("start up success!")
    