

<img align="right" width="200" alt="20200907_104224" src="./images/neolibcone.png">

# NeoLibrary 🍦

![neolibrary-Version: 0.2.1b1](https://img.shields.io/badge/neolibrary-0.2.1b1-informational?style=flat-square)
![PyPI status](https://img.shields.io/pypi/status/ansicolortags.svg)
![Coverage](./badges/rt-coverage-badge.svg)
![Flake8](./badges/rt-flake8-badge.svg)
![Test](./badges/rt-tests-badge.svg)

![Documenation](./images/documentation.png)

---

The documentation describes the purpose and how to use the neolib. This documenation is also purposely written in a cute format to make it more fun to read. Ice cream to everyone who reads it.


![Description](./images/description.png)

---

The neolib is a library for the common functions that is used in the NeoMedSystem projects.

![Description](./images/neologger.png)

---

NeoLogger is the logger component that is compliant with Grafana Loki https://grafana.com/oss/loki/ and is used to log all events in the NeoMedSys projects. The logger is based on the python logging library and is easy to use.

The logger will save a logger file in the /logs directory for each file that uses the logger. These logfiles are deleted when the rotation day is reached. The default rotation day is 30 days. The logfiles are saved in the /logs directory.

The logger is imported as;

```python
from neolibrary.monitoring.logger import NeoLogger
```

![Utils](./images/utils.png)

---

Utils contains all the utility functions that is used in the NeoMedSys projects. Such as hash functions, datetime cleanup, etc.

utils are imported as;

```python
import neolibrary.utils as utils
```

![Description](./images/decorators.png)

---

Decorators contains all the decorators that is used in the NeoMedSys projects. Such as timer, etc. These are special functions that can be used to decorate other functions such as shown below:

```python
@timer
def my_function():
    pass
```

decorators are imported as;

```python
from neolibrary.decorators import timer
```

![Blazing](./images/blazing.png)

---

It is super easy to add logger to your project. Just add the following code to your project and you are good to go.

Use your favorite *package manager*. Here at NeoMedSys we use poetry.
```shell
$ poetry add neolibrary
```

Then add the following code below to your project. This enabled the logger with log rotation of 30 days (resets the logger for memory cleanup). The default is 30 days.

```python
from neolibrary.monitoring import NeoLogger

logger = NeoLogger(__name__, rotate_days=30)
```


The library contains all functions that the the NeoMedSys pythonased project needs, such as:

```python
from neolibrary.utils import my_function

something = my_function()
```

Neolibrary also contains functions for preprocessing data, such as:

```python
from neolibrary.preproc import zscore

znorm = zscore(data)
```

See full documentation to see all functionality


![Description](./images/workflow.png)

---

This package uses Github workflow for CI/CD. Publication to pypi happens if a new release is created, except if the version includes *alpha* at the end of the version number. 

The version should be changed in the pyproject.toml file. The version number should follow the [Semantic Versioning](https://semver.org/) standard.
