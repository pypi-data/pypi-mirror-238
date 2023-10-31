import numpy as np

from wuncolors.color import Color
from wuncolors.formats import RGB


def fader(left: Color, right: Color, mix: float = 0.) -> Color:
    c1 = np.array(left.rgba())
    c2 = np.array(right.rgba())
    fade = ((1 - mix)*c1 + mix*c2)
    return Color(f"{left.name}({1-mix}) * {right.name}({mix})", RGB(*fade.tolist()))


def gradient(left: Color, right: Color, n: int = 100) -> list[Color]:
    grd = []
    for point in range(n):
        c = fader(left, right, point/n)
        grd.append(c)
        
    return grd
