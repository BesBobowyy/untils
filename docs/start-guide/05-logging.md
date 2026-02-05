# Logging

This is the last lesson in this course.

You can get logs by the library with Python's standard library `logging`.

All library logs may be accessed by `Settings.logger` property.

Code example:

```py
import untils

from typing import List

import logging
import os

# Logging settings.
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="./test.log",
    filemode='w',
    encoding='utf-8',
    level=logging.DEBUG,
    format="%(name)s %(asctime)s %(levelname)s %(message)s"
)

# Computing paths.
DIR: str = os.path.abspath(os.path.dirname(__file__))    # The 'Project' path.
CONFIG_PATH: str = os.path.join(DIR, "resources", "config.json")    # Hardcoded path.

# The library configuration.
settings: untils.Settings = untils.Settings()    # Context settings object.
command_system: untils.CommandSystem = untils.CommandSystem(settings)    # Command system.
command_system.load_config(CONFIG_PATH)    # Load the config.

print(settings.logger)    # A settings logger.
```

But you have print in work console by `warnings.warning` and exceptions.

## Conclusion

TL;DR: You can use the standard Python's `logging` library with `untils` logs.

You have complete this course, well done! Now you can write your console games or utils with the base library meaning. To see other courses or API Reference return to the main page.

## Documentation

[Home](../index.md "Home page.")

[API Reference](../api-reference.md "API Reference attachment.")
