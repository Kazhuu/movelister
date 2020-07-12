#! /usr/bin/python

"""
This script will package Movelister Python sources to be part of LibreOffice
Calc document.

Document will be packed with all Movelister Python source and it's manifest.xml
file modified to include all added file paths. This way the project can be
distributed just by sharing the document and sources only need to exists inside
that document. No system installation needed.

Tested to work on both Windows and Linux.
"""
import os
import argparse
import utils

from utils import Document, Manifest

# Add needed document argument.
parser = argparse.ArgumentParser()
parser.add_argument("document", help="document to update to use current Movelister Python source files")
args = parser.parse_args()

# Check that document exists.
if not os.path.exists(args.document):
    print('document "{0}" not found'.format(args.document))
    exit()
# Check that document is valid LibreOffice document.
if not utils.isValidLibreOfficeFile(args.document):
    print('file "{0}" is not a valid LibreOffice document'.format(args.document))
    exit()

# Collect paths to all source files in the project.
source_files = utils.collect_project_source_files()

# Read manifest.xml content, remove old source paths from it and add new ones.
manifest = Document.read_manifest_xml(args.document)
manifest = Manifest.remove_source_paths(manifest)
manifest = Manifest.add_python_source_folders(manifest)
manifest = Manifest.add_file_paths(manifest, source_files)

# Remove old manifest.xml and Python files from the document.
Document.remove_old_files(args.document)

# Add new manifest.xml to the document.
Document.write_manifest_xml(args.document, manifest)
# Add all Movelister source files to the document.
Document.add_files(args.document, source_files)

print('Movelister sources updated for document: {0}'.format(args.document))
