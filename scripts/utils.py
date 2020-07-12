"""
This file contain utility functions to manipulate LibreOffice document files and their content.
"""
import glob
import tempfile
import shutil
import os
import zipfile
import re
import posixpath
from pathlib import Path

# Project related paths.
PROJECT_ROOT_FOLDER = str(Path(os.path.dirname(os.path.realpath(__file__))).parent)
PROJECT_SOURCE_FILES_FOLDER = os.path.join(PROJECT_ROOT_FOLDER, 'pythonpath', 'movelister')

# Handled document files.
DOCUMENT_SCRIPTS_FOLDER = 'Scripts/'
DOCUMENT_PYTHON_FOLDER = '{0}python/'.format(DOCUMENT_SCRIPTS_FOLDER)
DOCUMENT_MANIFEST_PATH = 'META-INF/manifest.xml'

# Pattern to match to be deleted files from the document before new ones are
# added. Will match manifest.xml file and all Python source files under
# 'Scripts' folder.
OLD_FILE_PATTERN = re.compile(r'(^Scripts|^META-INF\/manifest\.xml$)')

def isValidLibreOfficeFile(file_path):
    """
    Return true if given file is valid LibreOffice ods file containing
    manifest.xml, false otherwise.
    """
    try:
        with zipfile.ZipFile(file_path, 'a') as open_document:
            open_document.open(DOCUMENT_MANIFEST_PATH)
        return True
    except KeyError:
        return False


def collect_project_source_files():
    """
    Collect all Movelister source file paths as array and return it.
    If executed on Windows then make sure paths are using '/' instead of '\'.
    This is needed because LibreOffice document's manifest.xml uses '/' slashes.
    """
    source_files = glob.glob(PROJECT_SOURCE_FILES_FOLDER + '/**/*.py', recursive=True)
    # Insert root main.py at the beginning.
    source_files.insert(0, os.path.join(PROJECT_ROOT_FOLDER, 'main.py'))
    return list(map(lambda path: posixpath.join(*path.split('\\')), source_files))


class Manifest:

    @classmethod
    def remove_source_paths(cls, manifest_xml_content):
        """
        Remove all Python source paths from the given manifest.xml content and
        return the modified content array.
        """
        manifest = []
        for line in manifest_xml_content:
            if 'Scripts' not in line:
                manifest.append(line)
        return manifest

    @classmethod
    def add_file_paths(cls, manifest_xml_content, python_file_paths):
        """
        Add given Python source file paths to manifest.xml so LibreOffice can
        find files correctly. Return new manifest content array.

        Given file paths are converted to use LibreOffice document file paths.
        Conversion is made based on the project root.
        """
        manifest = []
        for line in manifest_xml_content:
            if '</manifest:manifest>' in line:
                for path in python_file_paths:
                    # Path to LibreOffice document path and Unix style.
                    document_path = Manifest.file_path_to_document_path(path)
                    manifest.append(' <manifest:file-entry manifest:media-type="application/binary" manifest:full-path="{0}"/>\n'.format(document_path))
            manifest.append(line)
        return manifest

    @classmethod
    def add_python_source_folders(cls, manifest_xml_content):
        """
        Add Python source folder paths to the new manifest array and return it.
        Paths to add are 'Scripts/' and 'Scripts/python/'.

        Folder paths in the manifest are needed because if they don't exist, on
        saving the document LibreOffice will delete all Python files and remove
        them from the manifest.xml.
        """
        manifest = []
        for line in manifest_xml_content:
            if '</manifest:manifest>' in line:
                manifest.append(' <manifest:file-entry manifest:media-type="application/binary" manifest:full-path="{0}"/>\n'.format(DOCUMENT_SCRIPTS_FOLDER))
                manifest.append(' <manifest:file-entry manifest:media-type="application/binary" manifest:full-path="{0}"/>\n'.format(DOCUMENT_PYTHON_FOLDER))
            manifest.append(line)
        return manifest

    @classmethod
    def file_path_to_document_path(cls, source_file_path):
        """
        Convert given full file path to LibreOffice document Python source
        path. For example
        'programming/movelister/pythonpath/movelister/error.py' to
        'Scripts/python/pythonpath/movelister/error.py'
        Also converts Windows paths with \ to use / instead.
        """
        pattern = PROJECT_ROOT_FOLDER.replace('\\', r'/') + '/'
        file_path = re.sub(pattern, '', source_file_path)
        return '{0}{1}'.format(DOCUMENT_PYTHON_FOLDER, file_path)


class Document:

    @classmethod
    def remove_old_files(cls, document):
        """
        Remove old files from the document, including manifest.xml and all
        files residing under 'Scripts' folder. Based on:
        http://stackoverflow.com/questions/4653768/overwriting-file-in-ziparchive
        """
        tempdir = tempfile.mkdtemp()
        try:
            tempname = os.path.join(tempdir, 'new.zip')
            with zipfile.ZipFile(document, 'r') as zipread:
                with zipfile.ZipFile(tempname, 'w') as zipwrite:
                    for item in zipread.infolist():
                        # If pattern does not match then add file to the new zip file.
                        if not OLD_FILE_PATTERN.match(item.filename):
                            data = zipread.read(item.filename)
                            zipwrite.writestr(item, data)
            shutil.move(tempname, document)
        finally:
            shutil.rmtree(tempdir)

    @classmethod
    def add_files(cls, document, source_files):
        """
        Write given source files to the document. File paths are converted to
        user document path instead. This is done based on the project root
        path.
        """
        with zipfile.ZipFile(document, 'a') as open_document:
            for src_file in source_files:
                open_document.write(src_file, Manifest.file_path_to_document_path(src_file))

    @classmethod
    def read_manifest_xml(cls, document):
        """
        Read manifest.xml file to array and return it from given LibreOffice
        document.
        """
        manifest = []
        with zipfile.ZipFile(document, 'a') as open_document:
            for line in open_document.open(DOCUMENT_MANIFEST_PATH):
                manifest.append(line.decode('utf-8'))
        return manifest

    @classmethod
    def write_manifest_xml(cls, document, manifest_content):
        """
        Write manifest.xml file to document with given content. Old
        manifest.xml should be removed before calling this one.
        """
        with zipfile.ZipFile(document, 'a') as open_document:
            open_document.writestr(DOCUMENT_MANIFEST_PATH, ''.join(manifest_content))
