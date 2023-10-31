#!/usr/bin/env python

import sys
from termcolor import cprint
from .ttiparse import output_lines, COLORS

def main():

    file_path = sys.argv[1]
    with open(file_path, 'r') as file:
        for line in output_lines(file):
            for character, attributes in line:
                color = None if attributes.foreground == 0 else COLORS[attributes.foreground]
                highlight = None if attributes.background == 0 else f'on_{COLORS[attributes.background]}'
                attrs = []
                if attributes.flashing:
                    attrs.append('blink')
                if attributes.lining:
                    attrs.append('underline')
                # TODO: attributes.size
                cprint(character, color, highlight, attrs=attrs, end='')
            print()

if __name__ == '__main__':
    main()
