## Quick start

* Required: Python@3.12
* Project use pipenv to manage library

```bash
  pip install pipenv
```

* Clone project from github. 
```bash
  git clone <repo-name>
  cd <repo-name>
  pipenv install
```

* If version pipfile is missmatch then do this command 
```bash
  pipenv lock --clear
```

* If you already install dependencies. Run bash below to access virtual enviroment
```bash
  pipenv shell
```

* Generate and run migration
```bash
  alembic revision --autogenerate -m "Any name"
  alembic upgrade head
```

* Run project
* Create .env file in root folder. Then copy .env.example patse into ,env

```bash
  python src/main.py
```

## Advanced error handle

* Run project
```bash
  export QT_QPA_PLATFORM=xcb

```

## Design tool

* Required lib: python3-pyqt5 pyqt5-dev-tools qttools5-dev-tools 
* Open tool
```bash
  designer
```

* Convert UI file to Python file
```bash
  pyuic5 -o output.py input.ui
```

## Lint

* Run lint
```bash
  pylint src
```

* Fix lint error
```bash
  autopep8 --in-place --aggressive --aggressive -r src/
```

