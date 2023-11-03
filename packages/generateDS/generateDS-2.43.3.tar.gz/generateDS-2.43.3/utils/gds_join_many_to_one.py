#!/usr/bin/env python

"""
usage: gds_join_many_to_one.py [-h] [-p INFILE_PREFIX] [-f] [-v]
        in_directory_name out_file_name

synopsis:
  Join files created by gds_split_one_to_many.py into a single file.

positional arguments:
  in_directory_name     file name/path of input directory
  out_file_name         file name/path of gds module to be written

options:
  -h, --help            show this help message and exit
  -p INFILE_PREFIX, --infile-prefix INFILE_PREFIX
                        prefix for generated file names. default="gdsmodule"
  -f, --force           force overwrite output file. Existing file
                        will be over-written.
  -v, --verbose         print additional information

examples:
  python gds_join_many_to_one.py indirectory outfilename.py
  python gds_join_many_to_one.py indirectory outfile.py -p "myprefix" -v -f
"""


import sys
import os
import argparse
import json


def dbgprint(opts, msg):
    if opts.verbose:
        print(msg)


def join_and_write(opts):
    dbgprint(
        opts,
        f'generating: {opts.in_directory_name} --> "{opts.out_file_name}"')
    out_file_name = opts.out_file_name
    main_file_name = os.path.join(
        opts.in_directory_name, f'{opts.prefix}header.py')
    enum_file_name = os.path.join(
        opts.in_directory_name, f'{opts.prefix}enumclasses.py')
    infilenames = get_infilenames(opts)
    auxilliary_file_name = os.path.join(
        opts.in_directory_name, f'{opts.prefix}footer.py')
    with open(out_file_name, 'w') as outfile:
        with open(main_file_name, 'r') as infile:
            content = infile.read()
            outfile.write(content)
        # outfile.write('\n')
        with open(enum_file_name, 'r') as infile:
            content = infile.read()
            outfile.write(content)
        # outfile.write('\n')
        for infilename in infilenames:
            infilename = os.path.join(opts.in_directory_name, infilename)
            with open(infilename, 'r') as infile:
                content = infile.read()
                outfile.write(content)
                outfile.write('\n')
                outfile.write('\n')
        with open(auxilliary_file_name, 'r') as infile:
            content = infile.read()
            outfile.write(content)


def get_infilenames(opts):
    configfilename = os.path.join(opts.in_directory_name, 'config.json')
    with open(configfilename, 'r') as configfile:
        config = json.load(configfile)
    names = config['elementfilenames']
    return names


def main():
    description = """\
synopsis:
  Join files created by gds_split_one_to_many.py into a single file.
"""
    epilog = """\
examples:
  python gds_join_many_to_one.py indirectory outfilename.py
  python gds_join_many_to_one.py indirectory outfilename.py -p "myprefix" -v -f
"""
    parser = argparse.ArgumentParser(
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "in_directory_name",
        type=str,
        help="file name/path of input directory"
    )
    parser.add_argument(
        "out_file_name",
        type=str,
        help="file name/path of gds module to be written"
    )
    parser.add_argument(
        "-p", "--prefix",
        type=str,
        default="gdsmodule",
        help='prefix for generated file names.  default="gdsmodule"'
    )
    parser.add_argument(
        "-f", "--force",
        action="store_true",
        help=("force overwrite output file.  "
              "Existing file will be over-written."),
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="print additional information",
    )
    opts = parser.parse_args()
    if os.path.exists(opts.out_file_name):
        if opts.force:
            os.remove(opts.out_file_name)
        else:
            sys.exit(f'output file "{opts.out_file_name}" exists.  '
                     'Use -f/--force to delete and overwrite.')
    join_and_write(opts)


if __name__ == '__main__':
    main()
