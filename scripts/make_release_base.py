#! /usr/bin/python

"""
This script will make release template LibreOffice Calc document with a single
dummy main.py file included.

This release template is used later to make the actually release document
packing all project source files. A dummy main.py file is only packed so the
macros can be assigned to buttons beforehand. When the actual release is made
then this dummy main.py file will be changed to Movelister's actual main.py
file which in turn contains the real macros.
"""
import zipfile
import os
import shutil

import utils

dummy_main_file = os.path.join(utils.PROJECT_SCRIPTS_FOLDER, 'dummy_main.py')
document_dummy_main_file = 'Scripts/python/main.py'

# Remove old release base document if it exists.
if os.path.exists(utils.RELEASE_BASE_DOCUMENT):
    os.remove(utils.RELEASE_BASE_DOCUMENT)
# Copy release base ods file.
shutil.copyfile(utils.BASE_DOCUMENT, utils.RELEASE_BASE_DOCUMENT)

manifest = []
with zipfile.ZipFile(utils.RELEASE_BASE_DOCUMENT, 'a') as document:
    for line in document.open('META-INF/manifest.xml'):
        if '</manifest:manifest>' in line.decode('utf-8'):
            # Add folder paths where sources reside in the document.
            for path in ['Scripts/', 'Scripts/python/', document_dummy_main_file]:
                manifest.append(' <manifest:file-entry manifest:media-type="application/binary" manifest:full-path="{0}"/>\n'.format(path))
        manifest.append(line.decode('utf-8'))

# Remove old manifest.xml from release document.
utils.remove_from_zip(utils.RELEASE_BASE_DOCUMENT, 'META-INF/manifest.xml')

# Open release base document again and write new manifest.xml file and copy
# dummy_main.py into it.
with zipfile.ZipFile(utils.RELEASE_BASE_DOCUMENT, 'a') as document:
    document.writestr('META-INF/manifest.xml', ''.join(manifest))
    # Write dummy_main.py file.
    document.write(dummy_main_file, document_dummy_main_file)

print('Movelister release base made to: {0}'.format(utils.RELEASE_BASE_DOCUMENT))
