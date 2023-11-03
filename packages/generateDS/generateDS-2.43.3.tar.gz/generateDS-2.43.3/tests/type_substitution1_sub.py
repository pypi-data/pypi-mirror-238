#!/usr/bin/env python

#
# Generated  by generateDS.py.
# Python 3.11.5 (main, Sep  2 2023, 14:16:33) [GCC 13.2.1 20230801]
#
# Command line options:
#   ('--no-dates', '')
#   ('--no-versions', '')
#   ('--member-specs', 'list')
#   ('-f', '')
#   ('-o', 'tests/type_substitution2_sup.py')
#   ('-s', 'tests/type_substitution2_sub.py')
#   ('--super', 'type_substitution2_sup')
#   ('--always-export-default', '')
#   ('--preserve-cdata-tags', '')
#
# Command line arguments:
#   tests/type_substitution.xsd
#
# Command line:
#   generateDS.py --no-dates --no-versions --member-specs="list" -f -o "tests/type_substitution2_sup.py" -s "tests/type_substitution2_sub.py" --super="type_substitution2_sup" --always-export-default --preserve-cdata-tags tests/type_substitution.xsd
#
# Current working directory (os.getcwd()):
#   generateds
#

import os
import sys
from lxml import etree as etree_

import type_substitution2_sup as supermod

def parsexml_(infile, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        parser = etree_.ETCompatXMLParser()
    try:
        if isinstance(infile, os.PathLike):
            infile = os.path.join(infile)
    except AttributeError:
        pass
    doc = etree_.parse(infile, parser=parser, **kwargs)
    return doc

def parsexmlstring_(instring, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        try:
            parser = etree_.ETCompatXMLParser()
        except AttributeError:
            # fallback to xml.etree
            parser = etree_.XMLParser()
    element = etree_.fromstring(instring, parser=parser, **kwargs)
    return element

#
# Globals
#

ExternalEncoding = ''
SaveElementTreeNode = True

#
# Data representation classes
#


class animalCollectionTypeSub(supermod.animalCollectionType):
    def __init__(self, animal=None, **kwargs_):
        super(animalCollectionTypeSub, self).__init__(animal,  **kwargs_)
supermod.animalCollectionType.subclass = animalCollectionTypeSub
# end class animalCollectionTypeSub


class animalTypeSub(supermod.animalType):
    def __init__(self, name=None, extensiontype_=None, **kwargs_):
        super(animalTypeSub, self).__init__(name, extensiontype_,  **kwargs_)
supermod.animalType.subclass = animalTypeSub
# end class animalTypeSub


class dogTypeSub(supermod.dogType):
    def __init__(self, name=None, weight=None, size=None, **kwargs_):
        super(dogTypeSub, self).__init__(name, weight, size,  **kwargs_)
supermod.dogType.subclass = dogTypeSub
# end class dogTypeSub


class catTypeSub(supermod.catType):
    def __init__(self, name=None, personality=None, breed=None, **kwargs_):
        super(catTypeSub, self).__init__(name, personality, breed,  **kwargs_)
supermod.catType.subclass = catTypeSub
# end class catTypeSub


def get_root_tag(node):
    tag = supermod.Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = None
    rootClass = supermod.GDSClassesMapping.get(tag)
    if rootClass is None and hasattr(supermod, tag):
        rootClass = getattr(supermod, tag)
    return tag, rootClass


def parse(inFilename, silence=False):
    parser = etree_.ETCompatXMLParser(strip_cdata=False)
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'animalCollectionType'
        rootClass = supermod.animalCollectionType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='',
            pretty_print=True)
    return rootObj


def parseEtree(inFilename, silence=False):
    parser = etree_.ETCompatXMLParser(strip_cdata=False)
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'animalCollectionType'
        rootClass = supermod.animalCollectionType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    mapping = {}
    rootElement = rootObj.to_etree(None, name_=rootTag, mapping_=mapping)
    reverse_mapping = rootObj.gds_reverse_node_mapping(mapping)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        content = etree_.tostring(
            rootElement, pretty_print=True,
            xml_declaration=True, encoding="utf-8")
        sys.stdout.write(content)
        sys.stdout.write('\n')
    return rootObj, rootElement, mapping, reverse_mapping


def parseString(inString, silence=False):
    if sys.version_info.major == 2:
        from StringIO import StringIO
    else:
        from io import BytesIO as StringIO
    parser = etree_.ETCompatXMLParser(strip_cdata=False)
    rootNode= parsexmlstring_(inString, parser)
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'animalCollectionType'
        rootClass = supermod.animalCollectionType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='')
    return rootObj


def parseLiteral(inFilename, silence=False):
    parser = etree_.ETCompatXMLParser(strip_cdata=False)
    doc = parsexml_(inFilename, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'animalCollectionType'
        rootClass = supermod.animalCollectionType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from type_substitution2_sup import *\n\n')
        sys.stdout.write('import type_substitution2_sup as model_\n\n')
        sys.stdout.write('rootObj = model_.rootClass(\n')
        rootObj.exportLiteral(sys.stdout, 0, name_=rootTag)
        sys.stdout.write(')\n')
    return rootObj


USAGE_TEXT = """
Usage: python ???.py <infilename>
"""


def usage():
    print(USAGE_TEXT)
    sys.exit(1)


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        usage()
    infilename = args[0]
    parse(infilename)


if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    main()
