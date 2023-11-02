import os
import importlib
from colorama import init, Fore, Back, Style


class ChecksLoader:
    """
    Gathers all the checks from the checks directory
    """

    def __init__(self, root_dir, checks_dir):
        self.root_dir = root_dir
        self.checks_dir = checks_dir
        self.check_modules = []

    def _load_check_module(self, module_path):
        module_name = (
            module_path.replace(self.root_dir + "/", "")
            .replace("/", ".")
            .replace(".py", "")
        )
        module = importlib.import_module(module_name)
        return module

    def load_all(self):
        for dirpath, dirnames, filenames in os.walk(
            os.path.join(self.root_dir, self.checks_dir)
        ):
            for filename in filenames:
                if filename.endswith(".py") and filename != "__init__.py":
                    full_path = os.path.join(dirpath, filename)
                    module = self._load_check_module(full_path)
                    self.check_modules.append(module)

        print(f"✅ Loaded {len(self.check_modules)} checks")
        print(f"✅ Loaded checks")
        return self.check_modules
