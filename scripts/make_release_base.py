#! /usr/bin/python

"""
This script will make release template LibreOffice Calc document with a single
main.py file included.

This release template is used later to make the actually release document
packing all project source files. Dummy main.py file is only packed so the
macros can be assigned to buttons beforehand. When the actual release is made,
this dummy main.py file will be changed to Movelister's actual main.py
file which in turn contains the real macros.
"""
import zipfile
import os
import shutil

import utils
from utils import Document, Manifest

dummy_main_file = os.path.join(utils.PROJECT_SCRIPTS_FOLDER, 'dummy_main.py')

# Read manifest.xml content, remove old source paths from it and add new ones.
manifest = Document.read_manifest_xml(utils.BASE_DOCUMENT)
manifest = Manifest.remove_source_paths(manifest)
manifest = Manifest.add_file_paths(manifest, ['main.py',])

# Remove old manifest.xml and main.py files from the document.
Document.remove_old_files(utils.BASE_DOCUMENT)

# Add new manifest.xml and main.py files.
Document.write_manifest_xml(utils.BASE_DOCUMENT, manifest)
Document.add_file_as(utils.BASE_DOCUMENT, dummy_main_file, 'Scripts/python/main.py')

print('Movelister release base made to: {0}'.format(utils.BASE_DOCUMENT))
