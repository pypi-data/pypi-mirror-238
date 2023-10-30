![Static Badge](https://img.shields.io/badge/Python_&#x1F49F;-orange?style=flat-square&logo=python&logoColor=white) [![Static Badge](https://img.shields.io/badge/documentation-blue?style=flat-square&logo=github)](https://grenait.github.io/fastfeatureflag/) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fastfeatureflag?style=flat-square) ![GitHub last commit (branch)](https://img.shields.io/github/last-commit/GreNait/fastfeatureflag/trunk?style=flat-square&color=orange) ![PyPI - Downloads](https://img.shields.io/pypi/dm/fastfeatureflag?style=flat-square&color=orange)

[![PyPI version](https://badge.fury.io/py/fastfeatureflag.svg)](https://badge.fury.io/py/fastfeatureflag) ![pylint_badge](docs/badges/pylint.svg) ![unittest_badge](docs/badges/unittests.svg) ![mypy](docs/badges/mypy.svg)   ![PyPI - License](https://img.shields.io/pypi/l/fastfeatureflag)

FastFeatureFlag is a lightweight tool to generate and use feature flags. Build in python for python. The key components are:

- easy to add feature flag(s)
- easily activate/deactivate features
- naming/grouping flags
- define custom response for flagged features
- use environment variables as your on/off switch
- manage feature flags with a simple toml file
- define a shadow method which should be executed instead of your deactivated feature

# &#x1F6E0; Installation

```console
pip install fastfeatureflag
```

```console
poetry add fastfeatureflag
```

## &#127987; `flag` away ...

&#x1F4A1;  _Take a look at the decorator `feature_flag()` - that is all you need._

```python title="fast feature flags"
from fastfeatureflag.feature_flag import feature_flag

@feature_flag("off")
def broken_feature():
    return "I am broken"

broken_feature()
NotImplementedError: Feature not implemented
```
