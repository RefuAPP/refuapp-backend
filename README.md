# RefuAPP backend 🏠

## Summary
- [Installing the dependencies](#installing-dependencies-and-environment)

## Installing dependencies and environment:

> __Note__: Python version used in the project is 3.11

### Install the development and build dependencies 📦
```shell
pip install -r requirements.txt
```

### Install the git hooks for following the development standards 🧍
```shell
sudo npm install -g @commitlint/{config-conventional,cli}
pre-commit install && pre-commit autoupdate && pre-commit install --hook-type commit-msg
```
