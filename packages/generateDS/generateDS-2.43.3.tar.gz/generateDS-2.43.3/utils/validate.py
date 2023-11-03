#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
synopsis:
  Validate XML instance doc against an XML schema.

usage:
  python validate.py <schema-file> <xml-instance-file>

examples:
  python validate.py plants.xsd plants01.xml

more info:
  https://lxml.de/validation.html

notes:
  This small app basically does the same validation that is done
  by xmllint.  In fact, since this app is built on top of
  lxml and since xmllint and lxml are both built
  on top of libxml, it uses the same code to perform that
  validation.
"""


import sys
from lxml import etree


def validate(schemafilename, xmlinstancefilename):
    schema = etree.XMLSchema(file=schemafilename)
    parser = etree.XMLParser(schema=schema)
    try:
        etree.parse(xmlinstancefilename, parser=parser)
        print('file validates')
    except etree.XMLSyntaxError as exp:
        print(exp)
        print('file does not validate')


def main():
    args = sys.argv[1:]
    if len(args) != 2:
        sys.exit(__doc__)
    schemafilename = args[0]
    xmlinstancefilename = args[1]
    validate(schemafilename, xmlinstancefilename)


if __name__ == '__main__':
    main()
