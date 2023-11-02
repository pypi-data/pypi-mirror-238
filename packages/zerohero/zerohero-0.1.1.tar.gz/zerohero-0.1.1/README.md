# zerohero

Example:

```
from pprint import pprint
from zerohero import make_zero_shot_classifier

categories = ["cat", "dog", "mouse", "human"]
zsc = make_zero_shot_classifier(
    categories=categories,
    model_type="sentence-transformers",
    model_name="paraphrase-albert-small-v2",
)
cat_text = (
    """The cat (Felis catus),
    commonly referred to as the domestic cat or house cat,
    is the only domesticated species in the family Felidae.
    """
    )

result = zsc(cat_text)

pprint(result)
```
## Development Instructions

Install Dependencies: `poetry install --with dev`  
Configure pre-commit hooks: `poetry run pre-commit install`  
Manually run black: `poetry run black zerohero/* tests/*`  
Manually run pylint: `poetry run pylint zerohero/* tests/*`
