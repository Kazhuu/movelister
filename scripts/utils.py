"""
File to hold general functions and constants only related to Python scripts in
scripts folder.
"""
import tempfile
import shutil
import os
import zipfile
import re
from pathlib import Path

PROJECT_ROOT_FOLDER = str(Path(os.path.dirname(os.path.realpath(__file__))).parent)
PROJECT_SOURCE_FILES_FOLDER = os.path.join(PROJECT_ROOT_FOLDER, 'pythonpath', 'movelister')
PROJECT_SCRIPTS_FOLDER = os.path.join(PROJECT_ROOT_FOLDER, 'scripts')
PROJECT_RELEASE_FOLDER = os.path.join(PROJECT_ROOT_FOLDER, 'releases')
PROJECT_TEMPLATE_FOLDER = os.path.join(PROJECT_ROOT_FOLDER, 'templates')

BASE_DOCUMENT = os.path.join(PROJECT_TEMPLATE_FOLDER, 'movelister_base.ods')
RELEASE_BASE_DOCUMENT = os.path.join(PROJECT_TEMPLATE_FOLDER, 'movelister_release_base.ods')
RELEASE_DOCUMENT = os.path.join(PROJECT_RELEASE_FOLDER, 'movelister.ods')
DOCUMENT_PYTHON_PATH = 'Scripts/python'

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

def file_path_to_document_path(source_file_path):
    """
    Convert given full file path to LibreOffice document Python source
    path. For example
    'programming/movelister/pythonpath/movelister/error.py' to
    'Scripts/python/pythonpath/movelister/error.py'
    """
    file_path = re.sub(PROJECT_ROOT_FOLDER, '', source_file_path)
    return '{0}{1}'.format(DOCUMENT_PYTHON_PATH, file_path)
