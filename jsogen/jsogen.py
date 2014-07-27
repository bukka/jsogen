#!/usr/bin/env python
import os
import sys
import argparse

def main(argv=False):
    argv = (argv or sys.argv)[1:]

    parser = argparse.ArgumentParser(description='JavaScript Object Generator')

    parser.add_argument('template',
                        help='template file or directory')
    parser.add_argument('-s', '--seed', type=int,
                        help='random generator seed value')

    args = parser.parse_args(argv)

    print(args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
