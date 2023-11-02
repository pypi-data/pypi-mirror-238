import json
import requests
import toml

try:
    from packaging.version import parse
except ImportError:
    from pip._vendor.packaging.version import parse

from colorama import init, Fore, Style


def current():
    return toml.load("pyproject.toml")["tool"]["poetry"]["version"]


def check():
    if last() > parse(current()):
        print(
            f"{Fore.YELLOW}A new release of unctl is available: {Fore.RED + Style.BRIGHT}{current()}{Style.RESET_ALL} -> {Fore.GREEN + Style.BRIGHT}{last()}{Style.RESET_ALL}"
        )
        print(
            f"{Fore.YELLOW}To update, run: {Fore.GREEN + Style.BRIGHT}pip install --upgrade unctl{Style.RESET_ALL}"
        )


def last():
    """Return version of package on pypi.python.org using json."""
    url = f"https://pypi.python.org/pypi/{__package__}/json"
    req = requests.get(url)
    version = parse("0")
    if req.status_code == requests.codes.ok:
        j = json.loads(req.text.encode(req.encoding))
        releases = j.get("releases", [])
        for release in releases:
            ver = parse(release)
            if not ver.is_prerelease:
                version = max(version, ver)
    return version
