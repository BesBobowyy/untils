# Welcome to untils

Welcome to untils! This light-weight library was made for console games and small utils, which can parse a raw config to commands, which can be accessed by user input and API. It supports a dependency-module config commands system, almost-perfect validation, states system, 4 command types.

With this library you has:

- Module-based config in markup line.
- Custom logic in OOP.
- Validation and parsing user input for 10 lines.
- Process exceptions.
- Almost-perfect detailed annotations everywhere.
- Fast command processing (~208µs).
- Infinitely extendable abilities.
- Calm about anything.

## Architecture

This library was builded with next architecture:

![Architecture diagramm.](assets/diagramm0.svg)

## Installing

You can install the library from PyPi:

```bash
pip install untils
```

!!! warning "Warning"
    The supported minimal Python version is unknown. Versions `3.12+` are supported anyway.

Test template:

```py
# Written by untils v1.0.0r.

import untils

print("Version: ", untils.utils.Constants.VERSION, ", Latest config version: ", untils.utils.Constants.LATEST_CONFIG_VERSION, sep='')
```

## Conclusion

With this library you save your time, code functionality and nerves, but you works with already done format and logic.
> Think about project, not boilerplate.

## Documentation

[Start Course](start-guide/01-first-project.md "Beginner course into the library.")

[API Reference](api-reference.md "API Reference attachment.")
