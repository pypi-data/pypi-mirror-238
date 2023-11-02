## unctl

<!-- PROJECT LOGO -->
<br />
<div align="center">
    <a href="https://unskript.com/">
        <img src="images/logo.png" alt="Logo" width="80" height="80">
    </a>
    <p align="center">
    <a href="https://pypi.org/project/unctl/"><img alt="Python Version" src="https://img.shields.io/pypi/v/unctl.svg"></a>
    <a href="https://pypi.python.org/pypi/unctl/"><img alt="Python Version" src="https://img.shields.io/pypi/pyversions/unctl.svg"></a>
    <a href="https://pypistats.org/packages/unctl"><img alt="PyPI unctl downloads" src="https://img.shields.io/pypi/dw/unctl.svg?label=unctl%20downloads"></a>
</p>
</div>

<!-- TABLE OF CONTENTS -->
<br />
<p align="center">Table of Contents</p>
<ol>
<li>
    <a href="#about-the-project">About The Project</a>
    <ul>
        <li><a href="#built-with">Built With</a></li>
    </ul>
</li>
<li>
    <a href="#getting-started">Getting Started</a>
    <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#development">Development</a></li>
        <li><a href="#release">Release</a></li>
    </ul>
</li>
<li><a href="#usage">Usage</a></li>
<li><a href="#roadmap">Roadmap</a></li>
<!-- <li><a href="#contributing">Contributing</a></li>
<li><a href="#license">License</a></li> -->
<li><a href="#contact">Contact</a></li>
<!-- <li><a href="#acknowledgments">Acknowledgments</a></li> -->
</ol>

<!-- ABOUT THE PROJECT -->
## About The Project

`unctl` is a versatile command-line tool designed to perform a wide range of checks and inspections on various components of your infrastructure. It provides a unified interface to assess the health and performance of different services and platforms, and goes beyond mere diagnosis. With built-in **AI** capabilities, it guides you seamlessly from system diagnostic to remediation, offering intelligent solutions to address any issues it detects.

This addition emphasizes the tool's capacity to not only identify problems but also provide **AI-driven** recommendations and solutions for resolving those issues, making it even more valuable for infrastructure management and maintenance.

| Provider | Checks |
|---|---|
| Kubernetes | 19 |
| Elastic Search | TBA |
| Postgres | TBA |
| AWS | TBA |
| GCP | TBA |

<p align="right">(<a href="#unctl">back to top</a>)</p>

### Built With

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)

<p align="right">(<a href="#unctl">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites
* Python >= 3.10
* [OpenAI API Key](https://platform.openai.com/account/api-keys) - to have AI based functionality enabled

### Installation

1. Get distibution on your machine:
    * Run `pip` command to install `unctl` from [PyPI](https://pypi.org/project/unctl/)
        ```sh
        pip install unctl
        ```
2. (optional) Set OpenAI API key to be able to use `--explain (-e)` option
   ```sh
   export OPENAI_API_KEY=<your api key>
   ```
2. (optional) Set `KUBECONFIG` variable to specific location other than default
   ```sh
   export KUBECONFIG=<path to kube config file>
   ```

### Development
1. Install [poetry](https://python-poetry.org/):
    ```sh
    pip install poetry
    ```
2. Enter virtual env:
    ```sh
    poetry shell
    ```
3. Install dependencies:
    ```sh
    poetry install
    ```
4. Run tool:
    ```sh
    python unctl.py -h
    ```
5. Format all files before commit changes:
    ```sh
    black .
    ```

### Release

For the release this repo is using [Semantic Realese](https://semver.org/) as automated process. To be able to generate changelogs we should keep using [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) practice. When PR merged to `master` it uses `squash and merge` with PR title for the commit message. This requires `PR title` to be conventional:
```
feat(EN-4444): Add Button component
^    ^          ^
|    |          |__ Subject
|    |_______ Scope
|____________ Type
```

When release job is running it will automatically bump up version depends on the changes:

1. `BREAKING CHANGE: <message>` - creates new major version
2. `feat: <message>` - creates new minor version
3. `fix or perf: <message>` - creates new patch version
4. [All other tags](https://python-semantic-release.readthedocs.io/en/latest/configuration.html#commit-parser-options-dict-str-any) will not create new release


<p align="right">(<a href="#unctl">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

```sh
% unctl -h
usage: unctl [-h] [-s] [-f] [-d] [-e] [-r] [-c] [-v]

Welcome to unSkript CLI Interface

options:
  -h, --help          show this help message and exit
  -s, --scan          Run a k8s scan
  -f, --failing-only  Show only failing checks
  -d, --diagnose      Run fixed diagnosis
  -e, --explain       Explain failures using AI
  -r, --remediate     Create remediation plan
  -c, --check         Run a single check
  -v, --version       show program's version number and exit
```

<p align="right">(<a href="#unctl">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [ ] K8s checks - in progress
- [ ] Elastic Search checks
- [ ] Postgres checks
- [ ] AWS checks
- [ ] GCP checks

<p align="right">(<a href="#unctl">back to top</a>)</p>

<!-- CONTRIBUTING -->
<!-- ## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#unctl">back to top</a>)</p> -->

<!-- LICENSE -->
<!-- ## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#unctl">back to top</a>)</p> -->

<!-- CONTACT -->
## Contact

Abhishek Saxena: abhishek@unskript.com

Official website: https://unskript.com/

<p align="right">(<a href="#unctl">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
<!-- ## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#unctl">back to top</a>)</p> -->
