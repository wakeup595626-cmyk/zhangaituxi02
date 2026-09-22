import importlib.util
import os
import time


REMOTE_EXECUTION_PATH = (
    r"D:\Program Files\Epic Games\UE_5.8\Engine\Plugins\Experimental\PythonScriptPlugin"
    r"\Content\Python\remote_execution.py"
)


def load_remote_execution():
    spec = importlib.util.spec_from_file_location("ue_remote_execution", REMOTE_EXECUTION_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    remote_execution = load_remote_execution()
    remote = remote_execution.RemoteExecution()
    remote.start()
    try:
        deadline = time.monotonic() + 4.0
        while time.monotonic() < deadline and not remote.remote_nodes:
            time.sleep(0.1)
        print("CODEX_REMOTE_NODES={}".format(remote.remote_nodes))
    finally:
        remote.stop()


if __name__ == "__main__":
    main()
