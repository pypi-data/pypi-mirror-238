# Bash Menu Builder
![PyPI - Version](https://img.shields.io/pypi/v/bash-menu-builder?logo=pypi&logoColor=white)
![Python Version](https://img.shields.io/badge/Python-v3.9-orange?logo=python&logoColor=white)
![PyPI - License](https://img.shields.io/pypi/l/bash-menu-builder)
![PyPI - Downloads](https://img.shields.io/pypi/dm/bash-menu-builder)
![GitHub repo size](https://img.shields.io/github/repo-size/OleksiiPopovDev/Bash-Menu-Builder)

This package help you build menu for yours console scripts

[Installation](#installation) | [Usage](#usage) | [Draw menu](#draw-menu) | [How it works](#how-it-works)

## Installation
For install package to your project use this command:
```shell
pip3 install bash-menu-builder
```

## Usage
Script give opportunity use two type views of menu:
 - [Input Menu](#the-input-type-menu)
 - [Select Menu](#the-select-type-menu)

### The Input type Menu

```python
from bash_menu_builder import InputMenu, MenuItemDto


def banner_text() -> str:
    return 'I\'m Banner Text'

def function_one() -> None:
    print('Script One')

def function_two() -> None:
    print('Script Two')

def function_three() -> None:
    print('Script Three')

    
if __name__ == "__main__":
    InputMenu(
        menu=[
            MenuItemDto(title='Test', option='one', handler=function_one),
            MenuItemDto(title='Test2', option='two', handler=function_two),
            MenuItemDto(title='Test3', option='three', handler=function_three),
        ],
        banner=banner_text()
    )
```
#### View Menu
<img src="https://raw.githubusercontent.com/OleksiiPopovDev/Bash-Menu-Builder/main/doc/example-input.gif" alt="How it works" style="width:100%;" />

### The Select type Menu
```python
from bash_menu_builder import SelectMenu, MenuItemDto


def banner_text() -> str:
    return 'I\'m Banner Text'

def function_one() -> None:
    print('Script One')

def function_two() -> None:
    print('Script Two')

def function_three() -> None:
    print('Script Three')

    
if __name__ == "__main__":
    SelectMenu(
        menu=[
            MenuItemDto(title='Menu Item One', option='one', handler=function_one),
            MenuItemDto(title='Menu Item Two', option='two', handler=function_two),
            MenuItemDto(title='Menu Item Three', option='three', handler=function_three),
        ],
        banner=banner_text()
    )
```
#### View Menu
<img src="https://raw.githubusercontent.com/OleksiiPopovDev/Bash-Menu-Builder/main/doc/example-select.gif" alt="How it works" style="width:100%;" />

## Draw menu
The menu draw via class ``View`` which get params of array with DTOs and text of banner (optional)
The MenuItemDto have 3 params ``def __init__(self, title: str, option_name: str, handler: object):``
 - ``title: str`` - the title of menu item
 - ``option_name: str`` - the option name for call menu via console
 - ``handler: object`` - the handler of menu item. What exactly script do after select this menu item.

## How it works
After select menu number and press Enter will run script in function. When script finish process menu will draw again.

Also you can call script without drawing menu. Just set option when call python script file, ex. ``python3 main.py --three``
In this case will run script for menu **'Menu Item Three'**. When script finish process menu will not draw again and program will close.

<img src="https://github.com/OleksiiPopovDev/Bash-Menu-Builder/blob/main/doc/example-console.png?raw=true" alt="How it works" style="width:100%;" />