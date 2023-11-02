# zerohero

## Development Instructions

Install Dependencies: `poetry install --with dev`  
Configure pre-commit hooks: `poetry run pre-commit install`  
Manually run black: `poetry run black zerohero/* tests/*`  
Manually run pylint: `poetry run pylint zerohero/* tests/*`