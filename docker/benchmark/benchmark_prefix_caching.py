import subprocess
import json
import time
import toml



def run_benchmark(model_name, dataset_path, num_prompts,port):
    """运行基准测试."""
    command = [
        "python3",
        "benchmark/benchmark_serving.py",
        "--backend", "openai-chat",
        "--model", model_name,
        "--endpoint", "/v1/chat/completions",
        "--dataset-name", "sharegpt",
        # "--dataset-name", "sonnet",
        "--dataset-path", dataset_path,
        "--num-prompts", str(num_prompts),
        "--port", str(port)
    ]
    print(f"运行命令: {' '.join(command)}")  # 打印完整的命令

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()  # 获取输出和错误

    if process.returncode != 0:
        print(f"基准测试失败，退出代码: {process.returncode}")
        print(stderr.decode('utf-8'))
        return None  # Indicate failure

    output = stdout.decode('utf-8')
    print(output)


if __name__ == "__main__":
    MODEL_NAME = "Llama3.1-1B"
    DATASET_PATH = "benchmark/ShareGPT_V4.3_unfiltered_cleaned_split.json"
    NUM_PROMPTS = 200
    PORT = 6008

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

    benchmark_result = run_benchmark(MODEL_NAME, DATASET_PATH, NUM_PROMPTS, PORT)