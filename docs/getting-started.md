<style>
  :root {
    /* CUSTOM ACCENT COLORS */
    --n-color-accent: tomato;

    --md-primary-fg-color: tomato;
  }
</style>

For now, Napolitan is not provided as a package in PyPI because MicroPython doesn't support installing packages via PyPI and pip. You can copy the `docs/examples/napolitan` directory to your project and use it with setting the path to the `napolitan` files in your PyScript config file.

For example, you can write your `pyscript.toml` file like below.

```toml
packages = []

[files]
"napolitan/core.py" = "napolitan/core.py"
"napolitan/livingstandard.py" = "napolitan/livingstandard.py"
"napolitan/shoelace.py" = "napolitan/shoelace.py" # If you use Shoelace components
```

Or, you can refer the files in the [`docs/examples/napolitan`](https://github.com/i2y/napolitan/tree/main/docs/examples/napolitan) directory of Napolitan repo directly in your `pyscript.toml` file.

```toml
packages = []

[files]
"https://raw.githubusercontent.com/i2y/napolitan/main/docs/examples/napolitan/core.py" = "napolitan/core.py"
"https://raw.githubusercontent.com/i2y/napolitan/main/docs/examples/napolitan/livingstandard.py" = "napolitan/livingstandard.py"
"https://raw.githubusercontent.com/i2y/napolitan/main/docs/examples/napolitan/shoelace.py" = "napolitan/shoelace.py" # If you use Shoelace components
```

Then, you can import the Napolitan modules in your PyScript files.

```python
from napolitan.core import Component, Prop, register
from napolitan.livingstandard import div, span
from napolitan.shoelace import sl_button, sl_button_group, sl_icon, sl_card
```

The example above is the actual code snippet from example code in Napolitan repository.

!!! info
    The documentation of Napolitan is under construction. If you want to know more about Napolitan, please refer to the examples in the `examples` directory of the Napolitan repository.
