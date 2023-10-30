FastFeatureFlag is a lightweight tool to generate and use feature flags. Build in python for python. The key components are:

- easy to add feature flag
- easily activate/deactivate features
- naming/grouping flags
- define custom response for flagged features
- use environment variables as your on/off switch
- manage feature flags with a simple toml file

# :tools: Installation
---

```console
pip install fastfeatureflag
```

```console
poetry add fastfeatureflag
```

## :white_flag: `flag` away ...
---

!!! tip "take a look at the decorator `feature_flag()` - that is all you need."

```python title="fast feature flags"
from fastfeatureflag.feature_flag import feature_flag

@feature_flag("off")
def broken_feature():
    return "I am broken"

broken_feature()
NotImplementedError: Feature not implemented
```
