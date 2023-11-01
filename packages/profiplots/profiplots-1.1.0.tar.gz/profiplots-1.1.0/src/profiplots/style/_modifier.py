from profiplots import settings, theme
from profiplots.style import _utils


def colored() -> dict:
    """Changes color cycle to a colored type.

    ::: {.callout-important}

    This style is more-or-less for explorations. Finaliz visualizations should have all colors specified manually.

    :::

    Returns
    -------
    dict
        Dictionary containing the changed color cycle.

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
    (
        so.Plot(data=data, x="sex", y="survived", color="embark_town")
        .theme(pfs.colored())
        .add(so.Bar(alpha=1), so.Agg(), so.Dodge())
        .label(title="Survival of various groups of passengers")
    )
    ```

    """
    _utils.validate_active_style()

    return {"axes.prop_cycle": theme.COLOR_CYCLER[settings.active_theme], "image.cmap": "pf_blues"}


def grey() -> dict:
    """Changes color cycle to a grey type (no colors).

    Returns
    -------
    dict
        RC Dictionary containing the changed color cycle.

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
    (
        so.Plot(data=data, x="sex", y="survived")
        .theme(pfs.grey())
        .add(so.Bar(), so.Agg(), so.Dodge())
        .label(title="Survival of various groups of passengers")
    )
    ```
    """
    _utils.validate_active_style()

    return {"axes.prop_cycle": theme.GREY_CYCLER[settings.active_theme], "image.cmap": "pf_greys"}

def greyscale() -> dict:
    """Changes color cycle to a greyscale. Unlike `grey` style, it uses multiple shades of gray.

    Returns
    -------
    dict
        RC Dictionary containing the changed color cycle.

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
    (
        so.Plot(data=data, x="sex", y="survived", color="embark_town")
        .theme(pfs.greyscale())
        .add(so.Bar(alpha=1), so.Agg(), so.Dodge())
        .label(title="Survival of various groups of passengers")
    )
    ```
    """
    _utils.validate_active_style()

    return {"axes.prop_cycle": theme.GREYSCALE_CYCLER[settings.active_theme], "image.cmap": "pf_greys"}


def grid(x: bool | None = None, y: bool | None = None) -> dict:
    """Shows or hides grid in the image.

    Parameters
    ----------
    x : bool | None
        If True, then shows X grid. If False, hides it. If None, does nothing. Defaults to None.
    y : bool | None
        If True, then shows Y grid. If False, hides it. If None, does nothing. Defaults to None.

    Returns
    -------
    dict
        RC dictionary containing the new grid configuration.

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
    (
        so.Plot(data=data, x="age", y="fare")
        .theme(pfs.grid(x=True, y=True))
        .add(so.Dots())
        .label(title="Dependency between Age and Fare of Titanic passengers")
    )
    ```
    """
    _utils.validate_active_style()

    rc_dict = {}

    if x is True and y is True:
        rc_dict["axes.grid"] = True
        rc_dict["axes.grid.axis"] = "both"
    elif x is True:  # and y is False or None
        rc_dict["axes.grid"] = True
        rc_dict["axes.grid.axis"] = "x"
    elif y is True:  # and x is False or None
        rc_dict["axes.grid"] = True
        rc_dict["axes.grid.axis"] = "y"
    elif x is False and y is False:
        rc_dict["axes.grid"] = False
    else:
        # both are None => nothing changes
        pass

    return rc_dict


def ticks(x: bool | None = None, y: bool | None = None) -> dict:
    """Returns configuration of the plots that shows or hides ticks on x or y axis.

    Parameters
    ----------
    x : bool | None
        If True, then x axis ticks are shown. If False, they are hidden. If None, does nothing. Defaults to None.
    y : bool | None
        If True, then y axis ticks are shown. If False, they are hidden. If None, does nothing. Defaults to None.

    Returns
    -------
    dict
        Configuration of the plots that shows or hides ticks when applied.

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
    (
        so.Plot(data=data, x="age", y="fare")
        .theme(pfs.ticks(x=False, y=False))
        .add(so.Dots())
        .label(title="Dependency between Age and Fare.")
    )
    ```
    """
    _utils.validate_active_style()

    rc_dict = {}

    if x is not None:
        rc_dict.update({"xtick.top": False, "xtick.bottom": x, "xtick.labeltop": False, "xtick.labelbottom": x})
    if y is not None:
        rc_dict.update({"ytick.right": False, "ytick.left": y, "ytick.labelright": False, "ytick.labelleft": y})

    return rc_dict


def spines(
    left: bool | None = None, right: bool | None = None, top: bool | None = None, bottom: bool | None = None
) -> dict:
    """Adds or removes borders of the plots.

    Parameters
    ----------
    left : bool | None
        If True, then the left spine is added. If False, it is remoted. If None, nothing is altered. Defaults to None.
    right : bool | None
        If True, then the right spine is added. If False, it is remoted. If None, nothing is altered.. Defaults to None.
    top : bool | None
        If True, then the top spine is added. If False, it is remoted. If None, nothing is altered.. Defaults to None.
    bottom : bool | None
        If True, then the bottom spine is added. If False, it is remoted. If None, nothing is altered.. Defaults to None.

    Returns
    -------
    dict
        Configuration of the spines.

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
    (
        so.Plot(data=data, x="survived", y="sex")
        .theme(pfs.spines(left=True, right=True, top=True, bottom=True))
        .add(so.Bar(), so.Agg(), so.Dodge())
        .label(title="Survival of various groups of passengers")
    )
    ```
    """
    _utils.validate_active_style()

    rc_dict = {}

    if left is not None:
        rc_dict["axes.spines.left"] = left
    if right is not None:
        rc_dict["axes.spines.right"] = right
    if top is not None:
        rc_dict["axes.spines.top"] = top
    if bottom is not None:
        rc_dict["axes.spines.bottom"] = bottom

    return rc_dict
