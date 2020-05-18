import zipfile
import shutil
import os
import glob

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
# Collect paths to all source files of the project.
movelister_files = glob.glob('pythonpath/**/*.py', recursive=True)
movelister_files.append('main.py')
# Open release movelister.ods document and write Python source files to it.
# LibreOffice documents are zipped files.
with zipfile.ZipFile(RELEASE_DOCUMENT, 'a') as document:
    # Write Python source files to the document.
    for src_file in movelister_files:
        document.write(src_file, '{0}/{1}'.format(RELEASE_ROOT, src_file))
    # Modify manifest file to include all Python source files.
    manifest = []
    for line in document.open('META-INF/manifest.xml'):
        if '</manifest:manifest>' in line.decode('utf-8'):
            # Add folder paths where sources reside in the document.
            for path in ['Scripts/', 'Scripts/python/']:
                manifest.append(' <manifest:file-entry manifest:media-type="application/binary" manifest:full-path="{0}"/>\n'.format(path))
            # Add entries for all Python source files in the document.
            for path in movelister_files:
                manifest.append(' <manifest:file-entry manifest:media-type="application/binary" manifest:full-path="{0}/{1}"/>\n'.format(RELEASE_ROOT, path))
        manifest.append(line.decode('utf-8'))
    document.writestr('META-INF/manifest.xml', ''.join(manifest))
print('Movelister release made to: {0}'.format(RELEASE_DOCUMENT))
