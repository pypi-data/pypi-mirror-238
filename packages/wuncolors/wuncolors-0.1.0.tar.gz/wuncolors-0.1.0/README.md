# wuncolors

Help manipulate Color objects and use custom Color Palettes.

## Basic Usage

### ColorPalette Object
Contains a hierachy of colors.
```python
from wuncolors import ColorPalette

palette = ColorPalette.from_toml(full_path="palette_example.toml")
```
	Primary
	 - blue(0, 0, 255, 1.0)
	 - red(255, 0, 0, 1.0)
	Secondary
	 - random(100, 56, 1, 1.0)
	 - random2(222, 222, 7, 1.0)
	Others
	 - white(255, 255, 255, 1.0)

```python
from wuncolors import ColorPalette

palette = ColorPalette.from_toml(full_path="palette_example.toml")
blue = palette.get_primary("blue")
red = palette.all_colors("red")

all_primary = palette.get_primary()
all_secondary = palette.get_secondary()

all_colors = palette.all_colors()
print(all_primary)
```

    [blue(0, 0, 255, 1.0), red(255, 0, 0, 1.0)]

### Color objects
```python
from wuncolors import Color

blue = Color.from_tuple(name="blue", rgb=(0, 0, 255))
```

### Dynamic Usage
You can create a Palette from scratch and be save using the to_toml() method. Duplicate colors will be ignored if inserted in the same category. Colors are stored as sets in the palette.
```python
from wuncolors import Color, ColorPalette

p = ColorPalette("Example")
p.primary.add(Color.from_tuple("blue", (0, 0, 255)))
p.secondary.add(Color.from_tuple("blue", (0, 0, 255)))
p.others.add(Color.from_tuple("blue", (0, 0, 255)))

p.to_toml("test_palette.toml")
```
    ColorPalette(Example)
        Primary
         - blue(0, 0, 255, 1.0)
        Secondary
         - blue(0, 0, 255, 1.0)
        Others
         - blue(0, 0, 255, 1.0)
