"""
This Python script will pack all project source files inside LibreOffice calc
spreadsheet document. This way the project can be distributed just by sharing
the document and sources only exists inside that document. No system
installation needed.

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


def remove_from_zip(zipfname, *filenames):
    """
    Delete given filesnames from the given zipfile.
    http://stackoverflow.com/questions/4653768/overwriting-file-in-ziparchive
    """
    tempdir = tempfile.mkdtemp()
    try:
        tempname = os.path.join(tempdir, 'new.zip')
        with zipfile.ZipFile(zipfname, 'r') as zipread:
            with zipfile.ZipFile(tempname, 'w') as zipwrite:
                for item in zipread.infolist():
                    if item.filename not in filenames:
                        data = zipread.read(item.filename)
                        zipwrite.writestr(item, data)
        shutil.move(tempname, zipfname)
    finally:
        shutil.rmtree(tempdir)


RELEASE_FOLDER = 'releases'
BASE_DOCUMENT = os.path.join('templates', 'movelister_release.ods')
RELEASE_DOCUMENT = os.path.join(RELEASE_FOLDER, 'movelister.ods')
RELEASE_ROOT = 'Scripts/python'

# Create releases folder if it does not exist.
if not os.path.exists(RELEASE_DOCUMENT):
    os.mkdir(RELEASE_FOLDER)
# Remove old movelister release if it exists.
if os.path.exists(RELEASE_DOCUMENT):
    os.remove(RELEASE_DOCUMENT)
# Copy release base ods file.
shutil.copyfile(BASE_DOCUMENT, RELEASE_DOCUMENT)

# Collect paths to all source files in the project.
source_files = glob.glob('pythonpath/**/*.py', recursive=True)
movelister_files = ['main.py']
# If executed on Windows then make sure paths are using '/' instead of '\'.
# This is needed because LibreOffice document's manifest.xml uses '/' slashes.
movelister_files.extend([posixpath.join(*path.split('\\')) for path in source_files])

# Open release document and read manifest.xml to memory and add all project
# Python source files to it.
manifest = []
with zipfile.ZipFile(RELEASE_DOCUMENT, 'a') as document:
    for line in document.open('META-INF/manifest.xml'):
        if '</manifest:manifest>' in line.decode('utf-8'):
            # Add folder paths where sources reside in the document.
            for path in ['Scripts/', 'Scripts/python/']:
                manifest.append(' <manifest:file-entry manifest:media-type="application/binary" manifest:full-path="{0}"/>\n'.format(path))
            # Add entries for all Python source files in the document.
            for path in movelister_files:
                manifest.append(' <manifest:file-entry manifest:media-type="application/binary" manifest:full-path="{0}/{1}"/>\n'.format(RELEASE_ROOT, path))
        manifest.append(line.decode('utf-8'))

# Remove old manifest.xml from release document.
remove_from_zip(RELEASE_DOCUMENT, 'META-INF/manifest.xml')

# Open release document again and write new manifest.xml file and copy all
# project source files in there.
with zipfile.ZipFile(RELEASE_DOCUMENT, 'a') as document:
    document.writestr('META-INF/manifest.xml', ''.join(manifest))
    # Write Python source files to the document.
    for src_file in movelister_files:
        document.write(src_file, '{0}/{1}'.format(RELEASE_ROOT, src_file))

print('Movelister release made to: {0}'.format(RELEASE_DOCUMENT))
