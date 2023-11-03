# Pyxides

> Containers for the python sages 🏺✨📦

<!-- 
TODO
[![Build Status](https://travis-ci.com/astromancer/pyxides.svg?branch=master)](https://travis-ci.com/astromancer/pyxides)
[![Documentation Status](https://readthedocs.org/projects/pyxides/badge/?version=latest)](https://pyxides.readthedocs.io/en/latest/?badge=latest)
[![PyPI](https://img.shields.io/pypi/v/pyxides.svg)](https://pypi.org/project/pyxides)
[![GitHub](https://img.shields.io/github/license/astromancer/pyxides.svg?color=blue)](https://pyxides.readthedocs.io/en/latest/license.html)
 -->

`pyxides` is a python library for working with array-like object containers.


The name "pyxides" is the plural form of the Greek word "pyxis" (πυξίς), the
name for the decorated cylindrical [containers from
antiquity](https://en.m.wikipedia.org/wiki/Pyxides_(vessel)). The name felt
appropriate for a `python` library involving containers!

# Install

```shell
pip install pyxides
```

# Use


### Basic usage
The `containers` module contains some ready-made container classes that can be 
used directly:

```python
from pyxides.containers import ArrayLike1D


a = ArrayLike1D([1, 2, 3])
# it has the usual list-like methods for editing, and expanding
three = a.pop(-1)
a.append(id)
a.extend(['some', 'other', object])
# multi-indexing works
a[[0, 3, 5]]
```
    [1, <function id(obj, /)>, 'other']

### Type Enforcement
To construct a container that only allows certain types of objects:
```python
from pyxides.type_check import OfType

class Twinkie:
    """Yum!"""

class Box(list, OfType(Twinkie)):
    """So much YUM!"""

twinkies = Box()
twinkies.append(Twinkie()) # OK!
```  
Object other than `Twinkie`s, are not allowed in the container:
```python
twinkies.append(0)
```
    TypeError: Items in container class 'Box' must derive from  <class '__main__.Twinkie'>. Item 1  is of type <class 'int'>.

### Vectorization
TODO
<!-- ```python
from pyxides.


``` -->

### Grouping containers
TODO
<!-- ```python
from pyxides.


```   -->

<!-- For more examples see [Documentation]() -->

<!-- # Documentation -->

<!-- # Test

The [`test suite`](./tests/test_splice.py) contains further examples of how
`DocSplice` can be used.  Testing is done with `pytest`:

```shell
pytest pyxides
``` -->

# Contribute
Contributions are welcome!

1. [Fork it!](https://github.com/astromancer/pyxides/fork)
2. Create your feature branch\
    ``git checkout -b feature/rad``
3. Commit your changes\
    ``git commit -am 'Add some cool feature 😎'``
4. Push to the branch\
    ``git push origin feature/rad``
5. Create a new Pull Request

# Contact

* e-mail: hannes@saao.ac.za

<!-- ### Third party libraries
 * see [LIBRARIES](https://github.com/username/sw-name/blob/master/LIBRARIES.md) files -->

# License

* see [LICENSE](https://github.com/astromancer/pyxides/blob/master/LICENSE)

<!-- 
# Version
This project uses a [semantic versioning](https://semver.org/) scheme. The 
latest version is
* 0.0.1
 -->
