# Movelister

Movelister is a tool for creating various types of in-depth notes
about video game mechanics data in sheet form. This could include simple
move lists, detailed mechanics notes for glitchers or other type of tables which
model the limits of a game's potential interactivity.

**Movelister is a work in progress and can be used, but may contain bugs.**

## Table of Contents

<!-- vim-markdown-toc GFM -->

* [How To Use](#how-to-use)
* [Dependencies](#dependencies)
  * [Windows](#windows)
  * [Linux (Ubuntu and Arch)](#linux-ubuntu-and-arch)
* [How It Works](#how-it-works)
* [Contributing](#contributing)
  * [Linux (Ubuntu and Arch)](#linux-ubuntu-and-arch-1)
    * [Running Macros From LibreOffice](#running-macros-from-libreoffice)
    * [Running Macros From Separate Python Process](#running-macros-from-separate-python-process)
  * [Windows](#windows-1)
* [Testing](#testing)
  * [Running Tests](#running-tests)
* [Making Release Document](#making-release-document)
* [Resources](#resources)

<!-- vim-markdown-toc -->

## How To Use

Project is released as a LibreOffice document which has all project sources
embedded inside of it. Meaning no additional installation needed and your game
data can be shared just by sharing the document. Movelister is supported on both
Windows and Linux.

Before using Movelister check [dependencies](#dependencies) below like
downloading latest LibreOffice. Then to use Movelister download template
document from
[here](https://github.com/Kazhuu/movelister/raw/master/templates/movelister.ods)
and start glitching your game. To learn how to use Movelister, please read the
[manual](https://github.com/Kazhuu/movelister/blob/master/MANUAL.md).


## Dependencies

### Windows

On Windows install LibreOffice 5 or newer and you are able to use Movelister.
On Windows Python is included and self-contained with LibreOffice installation
so no separate Python installation needed.

### Linux (Ubuntu and Arch)

Install LibreOffice from sources or package repository

```
sudo apt install libreoffice
```

Movelister needs Python 3 to work properly. On Linux LibreOffice is using
system's Python installation. Meaning it's necessary to install Python if not
included in your system's installation. After that you need to install
LibreOffice Python support packages. On Ubuntu install following packages to
enable Python for LibreOffice:

```
sudo apt install libreoffice-script-provider-python uno-libs3 python3-uno
```

Arch installation has been tested to work out of the box.

## How It Works

Movelister is implemented on LibreOffice Calc (spreadsheet) and is used with
Python macros. Macros call further Python code which is responsible for
manipulating tables and sheets underneath. Python process responsible of
executing macros is communicating to LibreOffice process using socket. Socket
communication is handler by LibreOffice's UNO (Universal Network Objects)
interface. UNO interface is used to read and write sheet data.

## Contributing

If you want to contribute to Movelister then this section is for you.

To have a good development environment with debugging abilities. It's easier to
develop and run macros using separate Python process executed from command-line
which then connects to an external LibreOffice process using sockets. After you
are done with the development, you can run working scripts inside the
LibreOffice using it's own macro manager. [This Christopher Bourez's blog
post](http://christopher5106.github.io/office/2015/12/06/openoffice-libreoffice-automate-your-office-tasks-with-python-macros.html)
explains the idea and this same idea is used with this project.

Movelister is developed so that is support running macros from separate Python
process and from the LibreOffice itself. When running macros from separate
Python process, it doesn't matter where Movelister project is located because
Python connects to LibreOffice process through socket. When running macros from
LibreOffice itself, you need to tell LibreOffice where to find them. Easiest way
to do this is clone Movelister to your wanted location where you normally do
your development and then make symbolic link from LibreOffice user Python macros
folder to Movelister folder. This varies a little bit between the platforms and
is explained below for each platform.

### Linux (Ubuntu and Arch)

#### Running Macros From LibreOffice

LibreOffice user Python macros are located under
`~/.config/libreoffice/4/user/Scripts/python/`. This still holds true if you are
using LibreOffice version 6 and above. If you only have
folders up to `.../user/` then you can make folders `Scripts` and `python` with
`mkdir` program. After this `cd` into just created folders. Your path now
should be something like this:
`/home/username/.config/libreoffice/4/user/Scripts/python`. Now make symbolic
link to cloned Movelister folder with following and change `path_to_movelister`
to point to your cloned Movelister folder:

```
ln -s <path_to_movelister> movelister
```

Now in LibreOffice when you go to **Tools -> Macros -> Run Macro** and open **My
Macros**. You should see **movelister** as a listed macro package. Now open
**movelister** and select **main**. Then on the right you should see list of all
available macros which can be executed or mapped to keys.

#### Running Macros From Separate Python Process

In project root folder, start LibreOffice Calc process with:

```
libreoffice templates/movelister_test.ods --accept="socket,host=localhost,port=2002;urp"
```

This opens a socket connection with port 2002. Separate Python process can now
connect to this one using UNO interface. Now start Python process by running
`main.py` with:

```
python main.py
```

Edit `main.py` file at the bottom of the file to run macro you are trying to
develop.

### Windows

TODO: Fix this section!

To use LibreOffice Calc with a socket open, you have to start LibreOffice using
the parameter listed below.
For convenience's sake, you might want to include this parameter inside some
shortcut that starts LibreOffice.

```
--accept="socket,host=localhost,port=2002;urp"
```

If you use command line to run scripts, it's the easiest to just use
LibreOffice's own installed version of Python to run any Python scripts.
Otherwise Python may have difficulties finding the important UNO library. In
addition, you need to start running the scripts from the main Movelister
directory so that Python can find any related Movelister-modules as well.

This part of the process can be made a bit faster by writing an own .bat file
inside the Movelister main folder that starts main.py with LibreOffice's own
Python executable that's usually situated in *LibreOffice 5/Program/*. For
example:

```
..\..\..\..\program\python main.py
```

## Testing

Movelister has unit tests to test application functionality and are implemented
using Python's own [unittests](https://docs.python.org/3/library/unittest.html)
library and tests can be found under `test` folder of the project.

During testing Python process will spawn headless LibreOffice Calc process
accepting socket connections. This connection is then used with UNO interface to
communicate with LibreOffice process to verify application functionality.
During testing Python will instruct LibreOffice to reload the file between test
cases.

NOTE: Unit tests works on Linux but not fully on Windows. When you run all unit
tests on Windows, LibreOffice will show a dialog between test cases that the
file is already open and do you want to open file in read-only mode. When file
is opened in the read-only mode then tests that write data over UNO API will
fail to do so. And as a result unit test will report an error saying it didn't
see the data it was trying to write over UNO API. This read-only error when
reopening the file between test cases doesn't exist on Linux and no workaround
for this has been found yet. Running single unit test at the time on Windows
should work fine though.

### Running Tests

Before running tests you need to set `MV_LB_BIN` environment variable to point
to the LibreOffice executable. This is used to run LibreOffice during test. On
Linux for example:

```
export MV_LB_BIN="libreoffice"
```

and on Windows:

```
set MV_LB_BIN="C:\Program Files\LibreOffice 5\program\soffice.exe"
```

How to run tests depends your system you are using. With Linux LibreOffice is
using system's Python installation and on Windows LibreOffice comes with it's
own Python executable. On Linux you can just go to the project's root and run
tests with system's Python:

```
python -m unittest
```

Unfortunately on Windows things are not so simple.  On Windows you need to use
LibreOffice's own Python executable instead. This executable is located under
LibreOffice installation folder. From project's root you need to traverse path
to the LibreOffice Python executable and this path depends where you cloned this
project. In this case it might be easier to make a command line bat script to
run the tests. For example something like the following:

```
..\..\..\..\program\python.exe -m unittest
```

## Making Release Document

It's possible to pack Python source files be part of the LibreOffice document.
This way when file is shared the sources come with it. So no system installation
needed.

LibreOffice files are like zip files which consist of files and metadata xml
file named `manifest.xml`. This file contains list of paths of all files inside
the document. When Python source files are added to the document, manifest.xml
file also need to be edited to include paths of added files. If path is missing
then LibreOffice will not find the file. All Python files need to be placed
under `Scripts/python` subfolder of the document.

To automate above process project includes Python code under `scripts` folder.
To make a release document run

```
python scripts/make_release.py
```

This will update LibreOffice document at `templates/movelister.ods`
to include latest source files. After this document is ready to use Movelister
template for your game.

## Resources

* [LibreOffice Python Scripts Help](https://help.libreoffice.org/6.3/en-US/text/sbasic/python/main0000.html)
* [LibreOffice Wiki of Python applications](https://wiki.documentfoundation.org/Macros/Python_Design_Guide)
* [PyUno documentation](http://www.openoffice.org/udk/python/python-bridge.html).
* [Apache OpenOffice Developer's Guide](https://wiki.openoffice.org/wiki/Documentation/DevGuide/OpenOffice.org_Developers_Guide)
* [Old StarOffice Programmer's Tutorial](https://www.openoffice.org/api/basic/man/tutorial/tutorial.pdf)
for main knowledge about OpenOffice UNO (Universal Network Objects) technology and how to use it.
* [LibreOffice SDK API documentation](https://api.libreoffice.org/docs/idl/ref/index.html).
* [Jamie Boyle’s Cookbook](https://documenthacker.files.wordpress.com/2013/07/writing_documents-_for_software_engineers_v0002.pdf).
* [Christopher Bourez's blog post](http://christopher5106.github.io/office/2015/12/06/openoffice-libreoffice-automate-your-office-tasks-with-python-macros.html)
* [Development enviroment setup using pyenv](https://gist.github.com/thekalinga/b74056272cb1afdabf529a332ff0f517).
* [LibreOffice's own Python examples](https://cgit.freedesktop.org/libreoffice/core/tree/pyuno/demo)
* [How to pack Python script as part of the document](https://wiki.openoffice.org/wiki/Python_as_a_macro_language)
