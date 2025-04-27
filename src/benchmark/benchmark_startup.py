import subprocess
import threading

def start_script_in_container(container_name, script_path):
    # 启动容器中的脚本，并实时读取输出
    process = subprocess.Popen([
        "docker", "exec", container_name,
        "python3", script_path
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')

    for line in process.stdout:
        print(line.strip())

    for line in process.stderr:
        print(line.strip())

    # 等待容器执行完毕
    process.wait()

def main():
    container_name = "docker-llama3.1-1b-1"
    script_path_in_container = "benchmark/benchmark_prefix_caching.py"

    start_script_in_container(container_name, script_path_in_container)

if __name__ == "__main__":
    main()
