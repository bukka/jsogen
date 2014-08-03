#!/usr/bin/env python
import os
import sys
import argparse

class TemplateAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        path = values
        if os.path.isfile(path):
            self.checkReadAcces(path, 'file')
            setattr(namespace, self.dest, values)
        elif os.path.isdir(path):
            self.checkReadAcces(path, 'directory')
            setattr(namespace, self.dest, values)
        else:
            raise argparse.ArgumentTypeError("Template path '%s' is neither file nor directory" % path)

    def checkReadAcces(self, path, what):
        if not os.access(path, os.R_OK):
            raise argparse.ArgumentTypeError("Template %s path '%s' is not readable" % (what, path))


def main(argv=False):
    argv = (argv or sys.argv)[1:]

    parser = argparse.ArgumentParser(description='JavaScript Object Generator')

    parser.add_argument('template', action=TemplateAction,
                        help='template file or directory')
    parser.add_argument('-s', '--seed', type=int,
                        help='random generator seed value')
    parser.add_argument('-o', '--output', type=int,
                        help='random generator seed value')

    try:
        args = parser.parse_args(argv)
    except argparse.ArgumentTypeError as exc:
        print(exc)
        return -1

    print(args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
