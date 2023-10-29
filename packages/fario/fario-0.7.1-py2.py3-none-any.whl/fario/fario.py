#!/usr/bin/env python

import argparse
import sys

from __about__ import version
def call_fario_out(args):
    print(args)

def call_fario_in(args):
    import fario_in
    fario_in.main(args)

def main():
    parser = argparse.ArgumentParser(prog='fario')
    parser.add_argument('--version', action='version', version='%(prog)s v'+version)
    subparser = parser.add_subparsers()

    fario_out = subparser.add_parser("out", description="Export Farcaster data.")
    fario_out.add_argument("fid", type=int, help="FID")
    fario_out.add_argument("--casts", help="User casts", action="store_true")
    fario_out.add_argument("--links", help="User links", action="store_true")
    fario_out.add_argument("--recasts", help="User recasts", action="store_true")
    fario_out.add_argument("--likes", help="User likes", action="store_true")
    fario_out.add_argument("--inlinks", help="Inbound links for user", action="store_true")
    fario_out.add_argument("--profile", help="User profile data", action="store_true")
    fario_out.add_argument("--all", help="Equivalent to --casts --links --recasts --likes --profile", action="store_true")
    fario_out.add_argument("--limit", type=int, help="Number of records. If more than one types of data are exported, the limit applies to each one separately.", default=sys.maxsize)
    fario_out.add_argument("--hub", help="Use the hub at <ADDRESS>. Ex. --hub 192.168.1.1:2283", type=str)
    fario_out.add_argument("--wait", type=int, help="Wait for <WAIT> milliseconds between reads.", default=0)

    fario_in = subparser.add_parser("in")
    fario_in.add_argument("fid", type=int, help="FID")
    fario_in.set_defaults(func=call_fario_in)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()