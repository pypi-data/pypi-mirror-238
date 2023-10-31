## Booting up the environment
---
In the root project folder
```bash
pip install poetry
```

To create your poetry environment
```bash
poetry shell
```
Store the command that will be printed in the output for later use
```bash
emulate bash -c '. /Users/aze/Library/Caches/pypoetry/virtualenvs/priori-tea-list-FeC8235P_-py3.8/bin/activate'
```
This will enable you to launch your poetry environment when necessary

To deactivate the environment
```bash
deactivate
```
To run the different tests/type hints, use the makefile such as 
```bash
make lint
```
The various commands can be seen in the Makefile