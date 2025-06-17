#!/usr/bin/env python

import sys

for index, arg in enumerate(sys.argv[1:], start=1):
    print(f'Argument {index}: "{arg}"')
