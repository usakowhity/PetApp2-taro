import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

try:
    # ★ ここを絶対パスにする
    controller_path = os.path.join(BASE_DIR, "controller.py")
    spec = None

    import importlib.util
    spec = importlib.util.spec_from_file_location("controller", controller_path)
    controller = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(controller)

    print("Loaded controller file:", controller.__file__)

except Exception as e:
    print("Import error:", e)
    raise

from controller import Controller

if __name__ == "__main__":
    controller = Controller()
    controller.run()

