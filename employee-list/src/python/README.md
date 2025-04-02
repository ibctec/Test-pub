# Employee list Application

Application can create employee and list employees stored in a local memory db

## Create DB: 
python -c "from emp.db import Base, engine; Base.metadata.create_all(bind=engine)"

## Run Application:
cd to python dir
poetry install
poetry run uvicorn emp.main:app --reload
Navigate to http://127.0.0.1:8000/docs and use the swagger docs

# Run with Docker
Navigate to python folder
docker build -f ../Docker/Dockerfile --progress=plain --no-cache  -t emp-app .
docker run --rm emp-app
Navigate to http://127.0.0.1:8000/docs and use the swagger docs


## Run Tests:
pytest tests/