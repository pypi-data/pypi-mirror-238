#!/usr/bin/env python

"""
usage: gds_one_to_many.py [-h] [-p OUTFILE_PREFIX] [-v] \\
          infilename outdirectoryname

synopsis:
  Split generated generateDS module into separate files (one per complexType).

positional arguments:
  infilename            file name/path of gds generated module
  out_directory_name    file name/path of output directory

options:
  -h, --help            show this help message and exit
  -p OUTFILE_PREFIX, --outfile-prefix OUTFILE_PREFIX
                        prefix for generated file names. default="gdsmodule"
  -v, --verbose         print additional information

examples:
  python gds_one_to_many.py infilename.py outdirectory
  python gds_one_to_many.py infilename.py outdirectory -p "myprefix"
"""


import sys
import os
import shutil
import argparse
import re
from enum import Enum, auto
import json


class FileStates(Enum):
    IN_PROLOG = auto()
    IN_IMPORTS = auto()
    IN_ENUM_CLASSES = auto()
    IN_DATA_REP_CLASSES = auto()
    IN_EPILOG = auto()


class ClassStates(Enum):
    BEFORE_BODY = auto()
    IN_BODY = auto()


Start_enum_pat = re.compile(r'^# Start enum classes$')
Start_data_repr_pat = re.compile(r'^# Start data representation classes$')
End_data_repr_pat = re.compile(r'^# End data representation classes.$')
Class_header_pat = re.compile(r'^class *(\w*)\((\w*)\):(.*)$')
End_class_pat = re.compile(r'^# end class \w*$')
Start_imports_etc_pat = re.compile(
    r'^# Namespace prefix definition table \(and other attributes, too\)$')


def dbgprint(opts, msg):
    if opts.verbose:
        print(msg)


def generate(opts):
    dbgprint(opts, f'generating -- from: "{opts.infilename}"')
    (prolog_lines,
     import_lines, enum_lines,
     data_repr_specs, footer_lines) = collect_lines(opts)
    write_lines(
        opts, prolog_lines,
        import_lines, enum_lines,
        data_repr_specs, footer_lines)


def collect_lines(opts):
    """Finite state machine whose purpose is to collect content
    """
    prolog_lines = []
    data_repr_specs = []
    import_lines = []
    enum_lines = []
    footer_lines = []
    with open(opts.infilename, "r") as infile:
        inlines = infile.readlines()
    file_state = FileStates.IN_PROLOG
    class_state = ClassStates.BEFORE_BODY
    line_idx = 0
    max_lines = len(inlines)
    while True:
        if line_idx >= max_lines:
            break
        elif file_state == FileStates.IN_PROLOG:
            if Start_imports_etc_pat.match(inlines[line_idx + 1]):
                file_state = FileStates.IN_IMPORTS
                prolog_lines.append(inlines[line_idx])
            else:
                prolog_lines.append(inlines[line_idx])
            line_idx += 1
        elif file_state == FileStates.IN_IMPORTS:
            if Start_enum_pat.match(inlines[line_idx + 1]):
                file_state = FileStates.IN_ENUM_CLASSES
                import_lines.append(inlines[line_idx])
            else:
                import_lines.append(inlines[line_idx])
            line_idx += 1
        elif file_state == FileStates.IN_ENUM_CLASSES:
            if Start_data_repr_pat.match(inlines[line_idx + 1]):
                enum_lines.append(inlines[line_idx])
                enum_lines.append(inlines[line_idx + 1])
                enum_lines.append(inlines[line_idx + 2])
                line_idx += 2
                file_state = FileStates.IN_DATA_REP_CLASSES
            else:
                enum_lines.append(inlines[line_idx])
            line_idx += 1
        elif file_state == FileStates.IN_DATA_REP_CLASSES:
            if End_data_repr_pat.match(inlines[line_idx + 1]):
                file_state = FileStates.IN_EPILOG
                #line_idx += 1
            else:
                if class_state == ClassStates.BEFORE_BODY:
                    if Class_header_pat.match(inlines[line_idx]):
                        mo = Class_header_pat.match(inlines[line_idx])
                        class_name, superclass_name, junk = mo.groups()
                        entry = {
                            'class_name': class_name,
                            'superclass_name': superclass_name,
                            'lines': [],
                            }
                        dbgprint(opts, f'capturing -- class: {class_name}  '
                                 f'superclase: {superclass_name}')
                        data_repr_specs.append(entry)
                        class_body_lines = entry['lines']
                        class_body_lines.append(inlines[line_idx])
                        class_state = ClassStates.IN_BODY
                    else:
                        # class_body_lines.append(inlines[line_idx])
                        pass
                else:    # IN_BODY
                    if End_class_pat.match(inlines[line_idx]):
                        class_body_lines.append(inlines[line_idx])
                        class_state = ClassStates.BEFORE_BODY
                    else:
                        class_body_lines.append(inlines[line_idx])
                line_idx += 1
        elif file_state == FileStates.IN_EPILOG:
            footer_lines.append(inlines[line_idx])
            line_idx += 1
    return (
        prolog_lines,
        import_lines, enum_lines,
        data_repr_specs, footer_lines)


def write_lines(
        opts, prolog_lines,
        import_lines, enum_lines,
        data_repr_specs, footer_lines):
    """Write out the main file all element files.
    """
    outdir = opts.out_directory_name
    prefix = opts.prefix
    outpath = os.path.join(outdir, '__init__.py')
    with open(outpath, 'w') as mainoutfile:
        mainoutfile.write(f'# {outpath}\n')
    outpath = os.path.join(outdir, f'{prefix}header.py')
    enumoutpath = os.path.join(outdir, f'{prefix}enumclasses.py')
    footeroutpath = os.path.join(outdir, f'{prefix}footer.py')
    dbgprint(opts, f'generating -- to: "{outpath}"')
    with open(outpath, 'w') as mainoutfile:
        for line in prolog_lines:
            mainoutfile.write(line)
        for line in import_lines:
            mainoutfile.write(line)
    dbgprint(opts, f'generating -- to: "{footeroutpath}"')
    with open(footeroutpath, 'w') as footeroutfile:
        for line in footer_lines:
            footeroutfile.write(line)
    dbgprint(opts, f'generating -- to: "{enumoutpath}"')
    with open(enumoutpath, 'w') as enumoutfile:
        for line in enum_lines:
            enumoutfile.write(line)
    filenames = []
    for spec in data_repr_specs:
        lines = spec.get('lines')
        class_name = spec.get('class_name')
        filename = f'{prefix}_{class_name}.py'
        pathandname = os.path.join(outdir, filename)
        with open(pathandname, 'w') as outfile:
            for line in lines:
                outfile.write(line)
        filenames.append(filename)
    config = {'elementfilenames': filenames}
    configfilename = os.path.join(outdir, 'config.json')
    with open(configfilename, 'w') as configfile:
        json.dump(config, configfile, indent=1)


def main():
    description = """\
synopsis:
  Split generated generateDS module into separate files (one per complexType).
"""
    epilog = """\
examples:
  python gds_one_to_many.py infilename.py outdirectory
  python gds_one_to_many.py infilename.py outdirectory -p "myprefix"
"""
    parser = argparse.ArgumentParser(
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "infilename",
        type=str,
        help="file name/path of gds generated module"
    )
    parser.add_argument(
        "out_directory_name",
        type=str,
        help="file name/path of output directory"
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
        help=("force overwrite output directory.  "
              "Existing contents will be deleted."),
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="print additional information",
    )
    opts = parser.parse_args()
    dbgprint(opts, f'opts: {opts}')
    if os.path.exists(opts.out_directory_name):
        if opts.force:
            # delete the directory
            shutil.rmtree(opts.out_directory_name)
        else:
            sys.exit(f'output directory "{opts.out_directory_name}" exists.  '
                     'Use -f/--force to delete all contents.')
    os.mkdir(opts.out_directory_name)
    generate(opts)


if __name__ == '__main__':
    main()
