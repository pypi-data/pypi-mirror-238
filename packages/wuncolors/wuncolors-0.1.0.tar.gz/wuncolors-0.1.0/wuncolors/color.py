from pathlib import Path

import toml

from wuncolors.formats import ColorFormat, RGB


class Color:
    def __init__(self, name: str, fmt: ColorFormat) -> None:
        self.name = name
        self.fmt = fmt

    @classmethod
    def from_tuple(cls, name, rgb: tuple):
        return Color(name, RGB(*rgb))

    def __repr__(self) -> str:
        return f"{self.name}{self.fmt}"

    def rgb(self) -> tuple[float, float, float]:
        return self.fmt.rgb()

    def rgba(self) -> tuple[float, float, float, float]:
        return self.fmt.rgba()

    def decimal_rgb(self) -> tuple[float, float, float]:
        return self.fmt.decimal_rgb()

    def decimal_rgba(self) -> tuple[float, float, float, float]:
        return self.fmt.decimal_rgba()

    def hex(self) -> str:
        return self.fmt.hex()

    def __eq__(self, other) -> bool:
        if not isinstance(other, Color):
            return False

        if self.rgba() == other.rgba() and self.name.lower() == other.name.lower():
            return True
        if self.name.lower() == other.name.lower():
            return True

        return False

    def __hash__(self) -> int:
        return hash(self.decimal_rgba())


class ColorNotFoundError(Exception):
    def __init__(self, name: str, options: list[str]) -> None:
        super().__init__(f"Color '{name}' not found in ColorPalette. Choose from {options}")


class ColorPalette:
    def __init__(
            self,
            name: str,
            primary: list[Color] | None = None,
            secondary: list[Color] | None = None,
            others: list[Color] | None = None,
    ):
        self.primary = set(primary or [])
        self.secondary = set(secondary or [])
        self.others = set(others or [])
        self.name = name

    def __str__(self):
        s = f"ColorPalette({self.name})\n"
        s += "\tPrimary\n"
        for p in self.primary:
            s += f"\t - {p}\n"
        s += "\tSecondary\n"
        for p in self.secondary:
            s += f"\t - {p}\n"
        s += "\tOthers\n"
        for p in self.others:
            s += f"\t - {p}\n"
        return s

    def __repr__(self):
        return self.__str__()

    def to_toml(self, full_path: str | Path):
        with open(full_path, "w") as f:
            toml.dump(self.as_dict(), f)

    def as_dict(self):
        p = {
            "primary": {c.name: c.rgb() for c in self.get_primary()},
            "secondary": {c.name: c.rgb() for c in self.get_secondary()},
            "others": {c.name: c.rgb() for c in self.get_others()}
        }
        return p

    @classmethod
    def from_toml(cls, full_path: str | Path, name: str = ""):
        """
        Creates a palette object from a toml file. See example. RGB values have to be between 0 and 255
        [primary]
        color_name: [r, g, b]
        [secondary]
        secondary_color: [r, g, b]
        [others]
        other_color: [r, g, b]

        :param full_path: Path of the toml file
        :param name: name of the final palette object
        :return:
        """
        palette = toml.load(full_path)

        pal = ColorPalette(name=name)
        pal.primary = pal.primary.union({Color.from_tuple(name, rgb) for name, rgb in palette["primary"].items()})
        pal.secondary = pal.secondary.union({Color.from_tuple(name, rgb) for name, rgb in palette.get("secondary", {}).items()})
        pal.others = pal.others.union({Color.from_tuple(name, rgb) for name, rgb in palette.get("others", {}).items()})

        return pal

    def get_primary(self, name: str | None = None) -> Color | list[Color]:
        """
        Return the colors from its name, in the primary section of the palette. If name is None it returns all primary colors
        :param name:
        :return:
        """
        return self._find_in(name, options=self.primary)

    def get_secondary(self, name: str | None = None) -> Color | list[Color]:
        """
        Return the colors from its name, in the secondary section of the palette. If name is None it returns all secondary colors
        :param name:
        :return:
        """
        return self._find_in(name, options=self.secondary)

    def get_others(self, name: str | None = None) -> Color | list[Color]:
        """
        Return the colors from its name, in the others section of the palette. If name is None it returns all other colors
        :param name:
        :return:
        """
        return self._find_in(name, options=self.others)

    def all_colors(self, name: str | None = None) -> Color | list[Color]:
        """
        Return the colors from its name, from all sections of the palette. If name is None it returns all colors
        :param name:
        :return:
        """
        all_options = self.primary.copy()
        all_options.update(self.secondary)
        all_options.update(self.others)
        return self._find_in(name, options=all_options)

    @classmethod
    def _find_in(cls, name: str | None, options: set[Color]) -> Color | list[Color]:
        if name is None:
            return [*options]

        result = [c for c in options if name == c.name]
        if not result:
            raise ColorNotFoundError(name, options=[o.name for o in options])
        if len(result) == 1:
            return result[0]
        return result
