#!/usr/bin/env python
import os
import sys
import argparse

def main(argv=False):
    print 'JSOGen'
    
    argv = (argv or sys.argv)[1:]
    
    return 0

if __name__ == "__main__":
    sys.exit(main())