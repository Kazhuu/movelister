#! /usr/bin/python

"""
This script will make a release version of Movelister LibreOffice Calc document.

Release is made by packing all Movelister Python source files inside the
LibreOffice Calc document and it's manifest.xml file modified to include all
file paths. This way the project can be distributed just by sharing the
document and sources only need to exists inside that document. No system
installation needed.

Tested to work on both Windows and Linux.
"""
import os

import utils
from utils import Document, Manifest

# Check that release document exists.
if not os.path.exists(utils.RELEASE_DOCUMENT):
    print('release document missing: {0}'.format(utils.RELEASE_DOCUMENT))
    exit()

# Collect paths to all source files in the project.
source_files = utils.collect_project_source_files()

# Read manifest.xml content, remove old source paths from it and add new ones.
manifest = Document.read_manifest_xml(utils.RELEASE_DOCUMENT)
manifest = Manifest.remove_source_paths(manifest)
manifest = Manifest.add_file_paths(manifest, source_files)

# Remove old manifest.xml and Python files from the document.
Document.remove_old_files(utils.RELEASE_DOCUMENT)

# Add new manifest.xml to the document.
Document.write_manifest_xml(utils.RELEASE_DOCUMENT, manifest)
# Add all Movelister source files to the document.
Document.add_files(utils.RELEASE_DOCUMENT, source_files)

print('Movelister release made to: {0}'.format(utils.RELEASE_DOCUMENT))
