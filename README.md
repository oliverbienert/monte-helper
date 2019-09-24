# monte-helper

School and kindergarten management, address database.

## Installation

Clone the git repository, change into the project directory
and checkout development branch:

```bash
git clone git@github.com:oliverbienert/monte-helper.git
cd monte-helper
git checkout development
```

Create a virtual environment, then activate it and upgrade tools:
```bash
python3 -m venv ~/.virtualenvs/monte-helper
source ~/.venvs/monte-helper/bin/activate
pip install --upgrade pip setuptools wheel pathlib2
```

Install requirements into the just created virtualenv:
```bash
pip install -r requirements.txt
```
Be patient, building wxPython takes quite a bit of time...

Run the program with:
```bash
python program/montehelper/montehelper.py
```