# Chroma Console

Chroma console is a python package for adding color and style to terminal text output using ANSI escape codes.

## Installation

```shell
pip install chromaconsole
```

## Functions
```python
Style.disable()
Style.enable()
Style.reset()
Style.bold()
Style.faint()
Style.italic()
Style.underline()
Style.slow_blink()
Style.rapid_blink()
Style.reverse()
Style.hidden()
Style.strikethrough()
Style.not_bold()
Style.normal_intensity()
Style.not_italic()
Style.not_underline()
Style.not_blinking()
Style.proportional_spacing()
Style.not_reversed()
Style.reveal()
Style.not_strikethrough()
Style.not_proportional_spacing()
Style.overlined()
Style.not_overlined()
Style.minecraft(*args)
Color.text(*args)
Color.default_text()
Color.background(*args)
Color.default_background()
```

## Example usage

```python
from chromaconsole import Color, Style

print(f"{Color.text(r, g, b)}here is RGB colored text{Style.reset()}")
print(f"{Color.background(r, g, b)}here is RGB colored background{Style.reset()}")

print(f"{Color.text('#rrggbb')}here is HEX colored text{Style.reset()}")
print(f"{Color.background('#rrggbb')}here is HEX colored background{Style.reset()}")

print(f"{Style.bold()}Bold {Style.reset()}")
print(f"{Style.italic()}Italic {Style.reset()}")
print(f"{Style.underline()}Underline {Style.reset()}")
print(f"{Style.strikethrough()}Strikethrough {Style.reset()}")

print(f"{Style.bold()}{Style.italic()}bold+italic {Style.reset()}")
print(f"{Style.minecraft('§','§ahello §4world§r')}")
```

## .enable() and .disable():

After executing the `Style.disable()` command, the system will no longer apply coloring and styling to the content. To re-enable these features, simply use the `Style.enable()` command.

```python
#disable the coloring and styling
Style.disable()
print(f"{Color.text(r, g, b)}text without color and style{Style.reset()}")
Style.enable()
print(f"{Color.text(r, g, b)}text with color and style{Style.reset()}")
```