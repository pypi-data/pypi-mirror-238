# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

from matplotlib import font_manager
from MPSPlots.tools.directories import fonts_directory


__all__ = [  # from https://www.1001fonts.com/cmu-font.html
    # 'cmu.serif-roman',
    # 'cmu.serif-roman-with-minus',
    # 'cmu.serif-bold',
    # 'cmu.serif-italic',
]

for font in __all__:
    font_file = f'{font}.ttf'
    font_file = fonts_directory.joinpath(font_file)
    font_manager.fontManager.addfont(font_file)

if __name__ == '__main__':
    font_names = font_manager.get_font_names()

    for name in sorted(font_names):
        print(name)

# -
