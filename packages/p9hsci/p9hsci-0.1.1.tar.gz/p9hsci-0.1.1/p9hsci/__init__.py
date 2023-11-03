from itertools import cycle, islice
from typing import Any, Protocol, Sequence, overload
from copy import copy
from warnings import warn
import plotnine as p9

class theme_hsci(p9.theme_light):
    def __init__(self, base_size=12, base_family="sans"):
        """
        HSCI plotnine theme

        Args:
            base_size (int): The base font size to use.
            base_family (str): The base font family to use.
        """
        super().__init__(base_size, base_family)
        self += p9.theme(
            axis_ticks_length=0,
            strip_background=p9.element_blank(),
            strip_text=p9.element_text(colour="black")
        )

coloropt_palettes = dict(
    coloropt_normal6=["#4053D3", "#DDB310", "#B51D14", "#00BEFF", "#FB49B0", "#00B25D", "#CACACA"],
    coloropt_bright6=["#EFE645", "#E935A1", "#00E3FF", "#E1562C", "#537EFF", "#00CB85", "#EEEEEE"],
    coloropt_dark6=["#005900", "#000078", "#490D00", "#8A034F", "#005A8A", "#443500", "#585858"],
    coloropt_fancy6=["#56641A", "#C0AFFB", "#E6A176", "#00678A", "#984464", "#5ECCAB", "#CDCDCD"],
    coloropt_tarnish6=["#274D52", "#C7A2A6", "#818B70", "#604E3C", "#8C9FB7", "#796880", "#C0C0C0"],
    coloropt_normal12=["#EBAC23", "#B80058", "#008CF9", "#006E00", "#00BBAD", "#D163E6",
                       "#B24502", "#FF9287", "#5954D6", "#00C6F8", "#878500", "#00A76C", "#BDBDBD"]
)

def get_coloropt_pal(n: int, option="normal") -> list[str]:
    """
    Returns one of the coloropt (https://tsitsul.in/blog/coloropt/) palettes (as a list of colour codes

    Args:
        n (int): The min number of colors desired.
        option (str, optional): The colour palette option to use. Defaults to "normal".

    Returns:
        list[str]: A list of colour options.
    """
    if option == "normal" and n > 6:
        return coloropt_palettes['coloropt_normal12']
    elif option == "normal":
        return coloropt_palettes['coloropt_normal6']
    return coloropt_palettes[option]


class PaletteGetter(Protocol):
    def __call__(self, n: int) -> Sequence[Any]: ...

def _coloropt_pal(option="normal") -> PaletteGetter:
    def _coloropt_n_pal(n: int) -> Sequence[Any]:
        palette = get_coloropt_pal(n, option=option)
        n_values = len(palette)
        if n > n_values:
            warn(
                f"This palette returns a maximum of {n_values} distinct values. You have requested {n}.")
            return list(islice(cycle(palette), n))
        return palette
    return _coloropt_n_pal


class scale_colour_coloropt(p9.scales.scale.scale_discrete):
    _aesthetics = ["color"]

    def __init__(self, option: str = "normal", **kwargs):
        """plotnine colour scale using one of the coloropt (https://tsitsul.in/blog/coloropt/) palettes"""
        self.palette = _coloropt_pal(option=option)
        self.na_value = self.palette(6)[-1]
        super().__init__(**kwargs)


class scale_fill_coloropt(scale_colour_coloropt):
    _aesthetics = ["fill"]

class scale_coloropt(scale_colour_coloropt):
    _aesthetics = ["color", "fill"]

scale_color_coloropt = scale_colour_coloropt

class scale_colour_viridis_c(p9.scale_color_cmap):
    def __init__(self, option: str = "viridis", **kwargs):
        """plotnine colour scale using one of the coloropt (https://tsitsul.in/blog/coloropt/) palettes"""
        super().__init__(cmap_name=option, **kwargs)

scale_color_viridis_c = scale_colour_viridis_c

class scale_fill_viridis_c(scale_colour_viridis_c):
    _aesthetics = ["fill"]

class theme_hsci_discrete(theme_hsci):
    
    def __init__(self, base_size=12, base_family="sans", palette="normal"):
        """HSCI plotnine theme with an associated default discrete colour scale"""
        super().__init__(base_size, base_family)
        self.option=option

    @overload
    def __radd__(self, other: p9.ggplot) -> p9.ggplot:
        ...

    def __radd__(self, other: p9.ggplot) -> p9.ggplot:
        if 'color' in other.mapping:
            other.scales.append(scale_colour_coloropt(option=self.option))
        if 'fill' in other.mapping:
            other.scales.append(scale_fill_coloropt(option=self.option))
        return super().__radd__(other)

class theme_hsci_continuous(theme_hsci):
    def __init__(self, base_size=12, base_family="sans", palette="viridis"):
        """HSCI plotnine theme with an associated default continuous colour scale"""
        super().__init__(base_size, base_family)
        self.option=palette

    @overload
    def __radd__(self, other: p9.ggplot) -> p9.ggplot:
        ...

    def __radd__(self, other: p9.ggplot) -> p9.ggplot:
        if 'color' in other.mapping:
            other.scales.append(scale_colour_viridis_c(option=self.option))
        if 'fill' in other.mapping:
            other.scales.append(scale_fill_viridis_c(option=self.option))
        return super().__radd__(other)


__all__ = ["theme_hsci", "coloropt_palettes", "scale_colour_coloropt", "scale_fill_coloropt", "scale_coloropt", "scale_colour_viridis_c", "scale_fill_viridis_c", "theme_hsci_continuous", "theme_hsci_discrete"]