# Inoopa's helpers

This repo contains helper functions we use in all of our python projects.

# This is pushed publicly to Pypi, so NEVER commit any secret here!

## How to publish package to Pypi

After any code change, **update the package version** in [pyproject.toml](./pyproject.toml).

Then, at the root of the repo:

```bash
# Login to Pypi
poetry config pypi-token.pypi <Pypi API token here>

# Build project
poetry build

# Publish
poetry publish
```