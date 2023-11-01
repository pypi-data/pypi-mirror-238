<!--readme-about-start-->
# MONAPipe

MONAPipe stands for "Modes of Narration and Attribution Pipeline". It provides natural-language-processing tools for German, implemented in Python/spaCy. In addition to spaCy's default components, we add specific custom components and models for Digital Humanities and Computational Literary Studies.

MONAPipe originally was created in the project group of [MONA](https://www.uni-goettingen.de/de/mona/626918.html) and is now further developed within [Text+](https://www.text-plus.org/en/home/) infrastructure.
<!--readme-about-end-->


## Installation and Usage

Installation via ´pip´ is going to be added soon. Until then follow the installation instruction for developement.

Check the [usage docs](https://text-plus-collections.pages.gwdg.de/mona-pipe/getting_started/getting_started/) to get started.


## Developement

<!--readme-dev-start-->
Setup a development environment as follows:

1. Prerequisites
    - Python: >=3.7

2. Set-up a virtual environment:

```sh
python3 -m venv env
source env/bin/activate
```

3. Updgrade `pip`:

```sh
pip install --upgrade pip
```

4. Install `monapipe` in editable mode alongside with dev-requirements. Run in top-level folder:

```sh
pip install -r requirements.dev.txt -e .
```
<!--readme-dev-end-->


## License

Original parts are licensed under LGPL-3.0-or-later. Derivative code and integretated resources are licensed under the respective license of the original (see our section [LICENSES](LICENSES)). Documentation, configuration and generated code files are licensed under CC0-1.0.