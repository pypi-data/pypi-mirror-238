import subprocess


# FIXME; we need to implement dict based execution here
def execute_k8s_cli(cmd: str) -> str:
    # print(f"Executing command: {cmd}")
    result = subprocess.run(
        cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )

    if result.returncode != 0:
        print(
            f"Error({result.stderr.rstrip()}) executing command({cmd}) output: {result.stdout}"
        )
        return ""

    return result.stdout
