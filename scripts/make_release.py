#! /usr/bin/python

"""
This script will make a release version of Movelister LibreOffice Calc document.

Release is made by packing all Movelister Python source files inside the
LibreOffice Calc document. This way the project can be distributed just by
sharing the document and sources only need to exists inside that document. No
system installation needed.

LibreOffice files are like zip files which contains meta data xml file named
manifest.xml. This file contains list of all files inside the document. This
file is modified with this script and all project source files are added to it.
Also all project sources are copied under 'Scripts/python' subfolder of the
document.

Tested to work on both Windows and Linux.
"""
import zipfile
import tempfile
import shutil
import os
import glob
import posixpath

import utils

if not os.path.exists(utils.RELEASE_BASE_DOCUMENT):
    raise '{0} file does not exist. Run \'scripts/make_release_base.py\' script to generate one'.format(utils.RELEASE_BASE_DOCUMENT)
# Create releases folder if it does not exist.
if not os.path.exists(utils.RELEASE_DOCUMENT):
    os.mkdir(utils.PROJECT_RELEASE_FOLDER)
# Remove old movelister release if it exists.
if os.path.exists(utils.RELEASE_DOCUMENT):
    os.remove(utils.RELEASE_DOCUMENT)
# Copy release base ods file.
shutil.copyfile(utils.RELEASE_BASE_DOCUMENT, utils.RELEASE_DOCUMENT)

# Collect paths to all source files in the project.
source_files = glob.glob(utils.PROJECT_SOURCE_FILES_FOLDER + '/**/*.py', recursive=True)
# Insert root main.py at the beginning.
source_files.insert(0, os.path.join(utils.PROJECT_ROOT_FOLDER, 'main.py'))
# If executed on Windows then make sure paths are using '/' instead of '\'.
# This is needed because LibreOffice document's manifest.xml uses '/' slashes.
movelister_files = list(map(lambda path: posixpath.join(*path.split('\\')), source_files))

# Open release document and read manifest.xml to memory and add all project
# Python source files to it.
manifest = []
with zipfile.ZipFile(utils.RELEASE_DOCUMENT, 'a') as document:
    for line in document.open('META-INF/manifest.xml'):
        if '</manifest:manifest>' in line.decode('utf-8'):
            # Add folder paths where sources reside in the document.
            for path in ['Scripts/', 'Scripts/python/']:
                manifest.append(' <manifest:file-entry manifest:media-type="application/binary" manifest:full-path="{0}"/>\n'.format(path))
            # Add entries for all Python source files in the document.
            for path in movelister_files:
                manifest.append(' <manifest:file-entry manifest:media-type="application/binary" manifest:full-path="{0}"/>\n'.format(utils.file_path_to_document_path(path)))
        manifest.append(line.decode('utf-8'))

# Remove old manifest.xml and dummy main.py files from release document.
utils.remove_from_zip(utils.RELEASE_DOCUMENT, 'META-INF/manifest.xml', 'Scripts/python/main.py')

# Open release document again and write new manifest.xml file and copy all
# project source files in there.
with zipfile.ZipFile(utils.RELEASE_DOCUMENT, 'a') as document:
    document.writestr('META-INF/manifest.xml', ''.join(manifest))
    # Write Python source files to the document.
    for src_file in movelister_files:
        document.write(src_file, utils.file_path_to_document_path(src_file))

print('Movelister release made to: {0}'.format(utils.RELEASE_DOCUMENT))
