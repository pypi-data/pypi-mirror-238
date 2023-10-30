# Overview

```shell
pip install preserves
```

This package ([`preserves` on pypi.org](https://pypi.org/project/preserves/)) implements
[Preserves](https://preserves.dev/) for Python 3.x. It provides the core [semantics][] as well
as both the [human-readable text syntax](text) (a superset of JSON) and [machine-oriented
binary format](binary) (including
[canonicalization](https://preserves.dev/canonical-binary.html)) for Preserves. It also
implements [Preserves Schema](schema) and [Preserves Path](path).

 - Main package API: [preserves](api)

## What is Preserves?

{% include "what-is-preserves.md" %}

## Mapping between Preserves values and Python values

Preserves `Value`s are categorized in the following way:

{% include "value-grammar.md" %}

{% include "python-representation.md" %}

[semantics]: https://preserves.dev/preserves.html#semantics
