⚠️ This is a fork of the original GreatAI library by [@schmelczer](https://github.com/schmelczer/great-ai), maintained by ScoutinScience. Make sure to install [sis-great-ai](https://pypi.org/project/sis-great-ai/) from PyPI to use this distribution.

# <img src="https://raw.githubusercontent.com/scoutinscience/great-ai/main/docs/media/logo.png" alt="logo of great-ai" width=60 /> GreatAI

> Easily transform your prototype AI code into production-ready software.

[![PyPI version](https://badge.fury.io/py/sis-great-ai.svg)](https://badge.fury.io/py/sis-great-ai)
[![Downloads](https://pepy.tech/badge/sis-great-ai/month)](https://pepy.tech/project/sis-great-ai)
[![Docker Pulls](https://img.shields.io/docker/pulls/scoutinscience/great-ai)](https://hub.docker.com/repository/docker/scoutinscience/great-ai)
[![Test](https://github.com/scoutinscience/great-ai/actions/workflows/test.yml/badge.svg)](https://github.com/scoutinscience/great-ai/actions/workflows/test.yml)
[![Sonar line coverage](https://sonar.scoutinscience.com/api/project_badges/measure?project=great-ai&metric=coverage)](https://sonar.scoutinscience.com/dashboard?id=great-ai)
[![Sonar LoC](https://sonar.scoutinscience.com/api/project_badges/measure?project=great-ai&metric=ncloc)](https://sonar.scoutinscience.com/dashboard?id=great-ai)

Applying AI is becoming increasingly more accessible, but many case studies have shown that these applications are often deployed poorly. This may lead to suboptimal performance and to introducing unintended biases. GreatAI helps fix this by allowing you to easily transform your prototype AI code into production-ready software.

## Example

```sh
pip install sis-great-ai
```

Create a new file called `demo.py`

```python
from great_ai import GreatAI

@GreatAI.create
def greeter(name: str) -> str:
    return f"Hello {name}!"
```

Start it by executing `great-ai demo.py`, and find the dashboard at [http://localhost:6060](http://localhost:6060/dashboard).

![demo screen capture](https://raw.githubusercontent.com/scoutinscience/great-ai/main/docs/media/demo.gif)

That's it. Your GreatAI service is _nearly_ ready for production use. Many of the [SE4ML best practices](https://se-ml.github.io) are configured and implemented automatically (of course, these can be customised as well).

[Check out the full documentation here](https://great-ai.scoutinscience.com).

## Why is this GREAT?

![scope of GreatAI](https://raw.githubusercontent.com/scoutinscience/great-ai/main/docs/media/scope-simple.drawio.svg)

GreatAI fits between the prototype and deployment phases of your AI development lifecycle. This is highlighted in blue in the diagram. Here, several best practices can be automatically implemented, aiming to achieve the following attributes:

- **G**eneral: use any Python library without restriction
- **R**obust: have error-handling and well-tested utilities out-of-the-box
- **E**nd-to-end: utilise end-to-end feedback as a built-in, first-class concept
- **A**utomated: focus only on what actually requires your attention
- **T**rustworthy: deploy models that you and society can confidently trust

## Why GreatAI?

There are other existing solutions aiming to facilitate this phase. [Amazon SageMaker](https://aws.amazon.com/sagemaker) and [Seldon Core](https://www.seldon.io/solutions/open-source-projects/core) provide the most comprehensive suite of features. If you have the opportunity to use them, do that because they're great.

However, [research indicates](https://great-ai.scoutinscience.com) that professionals rarely use them. This may be due to their inherent setup and operational complexity. **GreatAI is designed to be as simple to use as possible.** Its straightforward, high-level API and sensible default configuration make it easy to start using. Despite its relative simplicity over Seldon Core, it still implements many of the [SE4ML best practices](https://se-ml.github.io), and thus, can meaningfully improve your deployment without requiring prohibitively great effort.

## [Learn more](https://great-ai.scoutinscience.com)

[Check out the full documentation here](https://great-ai.scoutinscience.com).

## Find `great-ai` on [PyPI](https://pypi.org/project/sis-great-ai/)

```sh
pip install sis-great-ai
```

## Find `great-ai` on [DockerHub](https://hub.docker.com/repository/docker/scoutinscience/great-ai)

```sh
docker run -p6060:6060 scoutinscience/great-ai
```

## Contribute

Contributions are welcome.

### Install for development

```sh
python3 -m venv --copies .env
source .env/bin/activate
pip install --upgrade flit pip
flit install --symlink
```

### Develop

```sh
scripts/format-python.sh great_ai docs tests
```

> Format code.

```sh
python3 -m pytest --doctest-modules --asyncio-mode=strict .
```

> Run tests.

```sh
mkdocs serve
```

> Serve documentation.
