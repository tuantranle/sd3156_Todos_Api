# FastAPI To dos application  
A FastAPI for To do sample application to learn how to use FastAPI with SQLAlchemy and PostGreSQL.

# Sample Setup 
- Create a virtual environment using `virtualenv` module in python.
```bash
# Install module (globally)
pip install virtualenv

# Generate virtual environment
virtualenv --python=<your-python-runtime-version> venv

# Activate virtual environment
source venv/bin/activate

# Install depdendency packages
pip install -r requirements.txt
```
- Configure `.env` file by creating a copy from `.env.sample`
- Dowload and install PostgreSQL from https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
- Using DBEaver to connect postgre and create database with name as `fastapi`
- At `app` directory, run `alembic` migration command. Please make sure your postgres DB is ready and accessible.
```bash
# Migrate to latest revison
alembic upgrade head

```
- Run `uvicorn` web server from `app` directory (`reload` mode is for development purposes)
```bash
uvicorn main:app --reload
```
