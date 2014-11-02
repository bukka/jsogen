#!/usr/bin/env python
import argparse
import os
from os.path import join
import sys
from template import Template

class TemplateGenerator:
    """Generate template from supplied arguments

    Template generator expects parameters processed
    by argparse in the main function."""

    def __init__(self, args):
        self.args = args

    def _generate(self, path=None, output=None):
        if not output:
            output = self.args.output
        if not path:
            path = self.args.template
        template = Template(path=path, output=output,
                            seed=self.args.seed, quiet=self.args.quiet)
        template.generate()

    def _walk(self):
        for root, dirs, files in os.walk(self.args.template_dir):
            root_common_dir = root[len(self.args.template_dir):]
            outdir = join(self.args.output_dir, root_common_dir)
            for tdir in (t for t in dirs if not os.path.isdir(join(outdir, t))):
                os.mkdir(join(outdir, tdir))
            for tfile in files:
                self._generate(join(root, tfile), join(outdir, tfile))

    def run(self):
        if self.args.template:
            self._generate(self.args.template, self.args.output)
        else:
            self._walk()


class TemplateAction(argparse.Action):
    """ArgumentParser action for template parameter"""

    def __call__(self, parser, namespace, values, option_string=None):
        path = values
        if os.path.isfile(path):
            self.checkReadAcces(path, 'file')
            setattr(namespace, self.dest, values)
        elif os.path.isdir(path):
            self.checkReadAcces(path, 'directory')
            setattr(namespace, self.dest + '_dir', values)
        else:
            raise argparse.ArgumentTypeError("Template path '%s' is neither file nor directory" % path)

    def checkReadAcces(self, path, what):
        if not os.access(path, os.R_OK):
            raise argparse.ArgumentTypeError("Template %s path '%s' is not readable" % (what, path))

class OutputAction(argparse.Action):
    """ArgumentParser action for template parameter"""

    def __call__(self, parser, namespace, values, option_string=None):
        path = values
        if os.path.isfile(path):
            self.checkWriteAcces(path, 'file')
            setattr(namespace, self.dest, values)
        elif os.path.isdir(path):
            self.checkWriteAcces(path, 'directory')
            setattr(namespace, self.dest + '_dir', values)
        else:
            dirname = os.path.dirname(path)
            if not os.path.isdir(dirname):
                raise argparse.ArgumentTypeError("Output path '%s' is neither file nor directory" % path)
            self.checkWriteAcces(dirname, 'parent directory')
            setattr(namespace, self.dest, path)

    def checkWriteAcces(self, path, what):
        if not os.access(path, os.W_OK):
            raise argparse.ArgumentTypeError("Output %s path '%s' is not writable" % (what, path))


def main(argv=False):
    argv = (argv or sys.argv)[1:]

    parser = argparse.ArgumentParser(description='JavaScript Object Generator')

    parser.add_argument('template', action=TemplateAction,
                        help='template file or directory')
    parser.add_argument('-s', '--seed', type=int,
                        help='random generator seed value')
    parser.add_argument('-o', '--output', action=OutputAction,
                        help='output file or directory')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='do not print any debug info')

    try:
        args = parser.parse_args(argv)
    except argparse.ArgumentTypeError as exc:
        print(exc)
        return -1

    # allow template directory only if output is set
    if not args.template and not "output_dir" in args:
        print("Output must be supplied if template is directory")
        return -1

    gen = TemplateGenerator(args)
    gen.run()

    return 0


if __name__ == "__main__":
    sys.exit(main())
