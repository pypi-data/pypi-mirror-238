# fake_session_maker

[![Latest Release](https://lab.frogg.it/dorianturba/fake_session_maker/-/badges/release.svg?order_by=release_at)](https://lab.frogg.it/dorianturba/fake_session_maker/-/releases)
[![Pipeline](https://lab.frogg.it/dorianturba/fake_session_maker/badges/main/pipeline.svg)](https://lab.frogg.it/dorianturba/fake_session_maker/-/pipelines)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/fake_session_maker.svg)](https://pypi.org/project/fake_session_maker)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/fake_session_maker)](https://pypi.org/project/fake_session_maker)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://lab.frogg.it/dorianturba/fake_session_maker/-/blob/main/LICENSE)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Markdown: pymarkdown](https://img.shields.io/badge/%20markdown-pymarkdown-%231674b1?style=flat&labelColor=ef8336)](https://github.com/jackdewinter/pymarkdown)

The `fake_session_maker` is a SQLAlchemy and Pytest-based package designed to facilitate
database testing by replacing a classic SQLAlchemy `SessionMaker` context manager.

## Features

- Replaces the SQLAlchemy `SessionMaker` context manager with a "read-only" session
  during tests.
- Rollbacks database state at the end of each test, ensuring isolation between tests.
- Simple fixture-based usage integrates smoothly with your Pytest suite.

## Drawbacks

Code that plan to be tested using `fake_session_maker` have the following limitations:

- Prevent the use of factory_boy automated build and bulk. Each object needs to be
  created and added to the session manually.

## Installation

```bash
pip install fake_session_maker
```

## Usage

### Define the fixture

Below is an example of how to use fake_session_maker in a pytest fixture:

```python
import pytest
from fake_session_maker import fsm


# Assuming Namespace is where the session_maker is defined

@pytest.fixture
def fake_session_maker():
    with fsm(
            db_url="sqlite:///tests/test.sqlite",
            namespace=Namespace,
            symbol_name="session_maker",
    ) as fake_session_maker_:
        yield fake_session_maker_

# Now, you can use fake_session_maker in your tests
```

### Use the fixture

Below is an example of how to use fake_session_maker fixture in a test:

```python
# Each test will have a fresh database, empty of any data
@pytest.mark.parametrize("name", ["jane", "joe"])
def test_create_example(fake_session_maker, name):
    result = create_example('test')
    assert result == 'success'
    with fake_session_maker() as session:
        # Each time we check, only the data created in this test will be present
        assert session.query(models.User).count() == 1
```

See
the [tests.test_fsm.py](https://lab.frogg.it/dorianturba/fake_session_maker/-/blob/main/tests/test_fsm.py)
directory for a full example.

## Contributing

Contributions are welcome! Please
see [CONTRIBUTING.md](https://lab.frogg.it/dorianturba/fake_session_maker/-/blob/main/CONTRIBUTING.md)
for more details.

## Testing

If you want to run the tests locally, you can follow instructions here:
[CONTRIBUTING.md #testing](https://lab.frogg.it/dorianturba/fake_session_maker/-/blob/main/CONTRIBUTING.md#testing).

## License

Distributed under the MIT License.
See [LICENSE](Lhttps://lab.frogg.it/dorianturba/fake_session_maker/-/blob/main/LICENSE)
for more information.
