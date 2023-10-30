# Ship It Validate

This package can be used to easily validate headers signed by [Ship It](https://ship-it.app).

## Install

```
pip install ship-it-validate
```

## Usage

Make sure to set the `SHIP_IT_PUBLIC_KEY` environment variable to the base64 encoded public key provided in the Ship It site configuration page.

### Flask

```python
from ship_it_validate import validate
from flask import request

@app.before_request
def before_request():
    try:
        validate(
            request.headers.get('X-PROXY-SIGNATURE'),
            request.headers.get('X-USER-SUB'),
            request.headers.get('X-PROXY-TIMESTAMP'),
        )
    except ValueError as e:
        app.logger.warning('Invalid Ship It signature: %s', e)
        return "Unauthorized", 401
```