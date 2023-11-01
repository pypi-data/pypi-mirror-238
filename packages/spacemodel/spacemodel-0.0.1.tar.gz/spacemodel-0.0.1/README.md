<div id="top"></div>

# SpaceModel

A wrapper providing Active-Record style access to Deta's Collections using Pydantic.

```py
from spacemodel import SpaceModel
from datetime import datetime


# The following is not required when ran inside a Deta Micro
SpaceModel.set_project_key('...')
# Or simply: os.environ['DETA_PROJECT_KEY'] = '...'

class Simple(SpaceModel, basename='my_collection'):
    name: str
    age: int

simple1 = Simple(name='alex', age=77)
simple1.save()

# Create to save it directly
simple2 = Simple.create({'name': 'alex', 'age': 77, 'key': 'one'})

# Expiring items
# Expire item in 300 seconds
simple3 = Simple(name='alex', age=77, key='alex23')
simple3.save(expire_in=300)

# Expire item at date
expire_at = datetime.fromisoformat('2023-01-01T00:00:00')
simple4 = Simple.create({'name': 'max', 'age': 28, 'key': 'max28'}, expire_at=expire_at)
```

refer to the [Space Docs](https://deta.space/docs/en/build/reference/sdk/base) for more information.

<div align="right">(<a href="#top">back to top</a>)</div>

<!-- LICENSE -->
## License
Distributed under the [Zero‐Clause BSD (0BSD)](https://opensource.org/license/0bsd/) license. See [LICENSE][license-url] for more information.

<div align="right">(<a href="#top">back to top</a>)</div>
