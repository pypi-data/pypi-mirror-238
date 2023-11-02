# Install package from GitHub

```shell
pip install git+https://github.com/Slamnlc/pytest_plugin_demo.git#subdirectory=pytest_my_cool_lib_demo
```

# Upload to Pypi

```shell
poetry publish --build --username __token__ --password pypi-AgEIcHlwaS5vcmcCJDJjYmEzMmYwLTEyM2QtNDU1Ni05ZWU4LWI1ZGY4NWUyYmZlNAACKlszLCJlNWQ3MmE4My1hNjlmLTRmMDQtOTc3Yi05YzI5MjgxNTc2MjMiXQAABiB2jldXiZpIKFFgI-rycwGAShDQ1ffciU278okUfK_7mQ
```

# Create release on GitHub (optional)

```shell
rm -rf dist
poetry build
gh release delete v$(poetry version -s) -y
gh release create v$(poetry version -s) dist/*.tar.gz --generate-notes
```

# Update version

```shell
poetry version minor
```
