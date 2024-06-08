poetry init
poetry shell
pyenv local 3.12.1
poetry env use 3.12.1
poetry add sqlalchemy
poetry add pydantic
poetry add fastapi
poetry add uvicorn
poetry add 'pydantic[email]'
poetry add psycopg2

docker compose up


