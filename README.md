## Quick start

* Required: Python@3.12
* Project use pipenv to manage library

```bash
  pip install pipenv
```

Clone project from github. 
```bash
  pipenv install <repo-name>
```

If you already install dependencies. Run bash below to access virtual enviroment
```bash
  pipenv shell
```

Generate and run migration
```bash
  alembic revision --autogenerate -m "Any name"
  alembic upgrade head
```

Run project
Create .env file in root folder. Then copy .env.example patse into ,env

```bash
  python src/main.py
```

## Advanced error handle

Run project
```bash
  export QT_QPA_PLATFORM=xcb

```

