# pydiff

## Installation

```
pip install -e .

```

## Usage

```python
from pydiff import resolve_diff
snippet_a = (
    "# Router definition",
    "api_router = APIRouter()"
)
snippet_b = (
    "# Make sure endpoint are immune to missing trailing slashes",
    "api_router = APIRouter(redirect_slashes=True)"
)
resolve_diff(snippet_a, snippet_b)

```

this gives

```
- api_router = APIRouter()
+ api_router = APIRouter(redirect_slashes=True)
```

## Development

```
# install dependencies
pip install -e '.[dev]'
pytest # run test
```
