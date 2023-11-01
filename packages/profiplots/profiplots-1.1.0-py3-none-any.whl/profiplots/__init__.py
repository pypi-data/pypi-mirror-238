"""
`profiplots` package enables us to use profinit plot styling in:

- `seaborn`,
- `matplotlib`.

The main function of this package is `set_theme`. It replaces default seaborn and matplotlib styling with our custom, Profinit styling. To try it out, just call:

```python
import profiplots as pf
pf.set_theme()
```

Now all `matplotlib` and `seaborn` plots will have our Profinit theme. These plots can be further customized. This is handled by submodules. Check out packages (and modules) `profiplots.style` and `profiplots.profile`. For even better control, we can use `profiplots.colors` to create perfectly colored plots.

"""

import matplotlib as _mpl
import matplotlib.pyplot as _plt
import seaborn.objects as _so

from profiplots import color, profile, settings, style, theme

__all__ = ["reset_theme", "set_theme", "set_style", "style_context", "style", "profile", "color", "settings", "theme"]

# register colormaps
_mpl.colormaps.register(color.GREY_CMAP, name="pf_greys", force=True)
_mpl.colormaps.register(color.BLUE_CMAP, name="pf_blues", force=True)
_mpl.colormaps.register(color.RED_CMAP, name="pf_reds", force=True)
_mpl.colormaps.register(color.BLUE_RED_CMAP, name="pf_blue_reds", force=True)

_orig_rc_config = _mpl.rcParams.copy()
"""Original rc settings before calling the first `set_theme`."""

class _RCAesthetics:
    """ """

    def __init__(self, **kwargs):
        self.config = kwargs

    def __enter__(self):
        self._orig = _mpl.rcParams.copy()
        _mpl.rcParams.update(self.config)
        _so.Plot.config.theme.update(self.config)

    def __exit__(self, exc_type, exc_value, exc_tb):
        _so.Plot.config.theme.update(self._orig)
        _mpl.rcParams.update(self._orig)



def set_theme(name: str = "default"):
    """Calling this function will set `profiplots` styling as the default styling for `matplotlib` and `seaborn` plots.

    Calling this function also defines following cmaps:

    - `pf_greys`,
    - `pf_blues`,
    - `pf_reds`,
    - `pf_blue_reds`.

    Their corresponding values can be found in `profiplots.color`.
    This function must be called before calling additional styling functions, like `colored`, `grid` etc.

    Parameters
    ----------
    name: str
        Name of the theme.

    Examples
    -------

    ```{python}
    #| echo: false
    import seaborn.objects as so
    import seaborn as sns
    data = sns.load_dataset("titanic")
    ```

    **No theme set**

    ```{python}
    (
        so.Plot(data=data, x="sex", y="survived")
        .add(so.Bar(), so.Agg())
        .label(title="Survival rate of titanic female passengers was significantly higher than male passengers")
    )
    ```

    **Profiplots theme**

    ```{python}
    import profiplots as pf

    # set theme
    pf.set_theme(name="default")

    (
        so.Plot(data=data, x="sex", y="survived")
        .add(so.Bar(), so.Agg())
        .label(title="Survival rate of titanic female passengers was significantly higher than male passengers")
    )
    ```
    """
    if name not in settings.SUPPORTED_THEMES:
        raise ValueError(f"Theme with name '{name}' is not supported.")

    # reset theme before setting up the new one
    reset_theme()

    # set up global themes
    _plt.style.use(f"profiplots.theme.{name}")
    _so.Plot.config.theme.update(_mpl.rcParams)

    settings.active_theme = name


def reset_theme():
    """Reset theme to previous defaults."""
    _mpl.rcParams.update(_orig_rc_config)
    _so.Plot.config.theme.update(_orig_rc_config)
    settings.active_theme = None


def style_context(rc_config: dict):
    """Alters default Profinit theme with new settings in a context window. Works both for `matplotlib` and `seaborn` (and `seaborn.objects.Plot`).

    Use this method instead of [mpl.rc_context](https://matplotlib.org/stable/api/matplotlib_configuration_api.html#matplotlib.rc_context).

    Parameters
    ----------
    rc_config : dict
        rc config values to be set for the duration of the context window.

    Examples
    -------

    ```{python}
    #| echo: false
    import seaborn.objects as so
    import seaborn as sns
    import profiplots as pf
    import profiplots.style as pfs

    data = sns.load_dataset("titanic")
    pf.set_theme(name="default")
    ```

    First let's look at what happens **inside** of the style context.

    ```{python}
    # Inside style context
    with pf.style_context(pfs.grid(x=True, y=True)):
        p = (
            so.Plot(data=data, x="age", y="fare")
            .add(so.Dots())
            .label(title="Title example")
            .plot()
        )
    p
    ```

    And now **outside** the default styles are being used..

    ```{python}
    # Inside style context
    p = (
        so.Plot(data=data, x="age", y="fare")
        .add(so.Dots())
        .label(title="Title example")
        .plot()
    )
    p
    ```
    """
    return _RCAesthetics(**rc_config)


def set_style(rc_config: dict):
    """Sets up the specific style permanently.

    Parameters
    ----------
    rc_config : dict
        rc config values to be set.

    Examples
    -------

    ```{python}
    #| echo: false
    import seaborn.objects as so
    import seaborn as sns
    import profiplots as pf
    import profiplots.style as pfs

    data = sns.load_dataset("titanic")
    pf.set_theme(name="default")
    ```

    ```{python}
    # set styles
    pf.set_style(pfs.colored())

    (
        so.Plot(data=data, x="age", y="fare", color="sex")
        .add(so.Dots())
    )
    ```
    """
    # set up global themes
    _plt.rcParams.update(**rc_config)
    _so.Plot.config.theme.update(_mpl.rcParams)
