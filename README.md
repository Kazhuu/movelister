# Movelister
Movelister is a tool for creating various types of in-depth notes
about video game mechanics data in sheet form. This could include simple
move lists, detailed mechanics notes for glitchers or other type of tables which
model the limits of a game's potential interactivity.


## Dependencies
It's necessary for the user to install LibreOffice 5 or newer and Python 3.x to be able
to use the Movelister scripts. Python is typically automatically included in a
LibreOffice installation on Windows but not on Linux. Linux users have to
install LibreOffice Python support packages separately. On Windows Python is
located with regular installation at `C:\Program Files\LibreOffice
5\program\python-core-3.5.0\bin\python.exe`. On Linux, install following
packages to enable Python for LibreOffice:
```
sudo apt install libreoffice-script-provider-python uno-libs3 python3-uno
```
On Linux distros that has both Python 2 and 3 versions available and command
`python` points to Python 2. Developers can change `python` commands to
`python3` in this readme instead.


## How to use
TODO: Write guide how to setup this project in order to use the template and

LibreOffice 5 has a specific directory where it searches for Python scripts -
something along the lines of *LibreOffice 5/share/Scripts/python*. If you copy
any Python scripts there, you are able to find & use them inside LibreOffice
via *Tools -> Macros -> Run Macro...* It's not a bad idea to copy the entire
Movelister directory inside *Scripts/Python* if you want to have access to all
the scripts and ensure that Movelister finds all its dependencies too.

__Note:__ so far the scripts are designed to be used together with the
Movelister template, so make sure that it's open in LibreOffice Calc before you
run scripts or you most likely get some errors.

__Note 2:__ since this project is still at its early stages, the scripts don't
offer a full functionality yet. Feel free to admire the template and give some
feedback or ideas on it, though.


rovided scripts.


## Development
To have a good development environment and with debugging abilities. It's
easier to develop scripts using a separate Python process which then connects to
an external LibreOffice process using sockets. After you are done with the
development, you can run working scripts inside the LibreOffice process. [This
Christopher
Bourez's blog
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


### Linux


#### Running macros from LibreOffice
LibreOffice user Python macros are located under
`~/.config/libreoffice/<version_number>/user/Scripts/python/`. If you only have
folders up to `.../user/` then you can make folders `Scripts` and `python` with
`mkdir` program. After this `cd` into just created python folder. You path now
should be something like this:
`/home/kazooie/.config/libreoffice/4/user/Scripts/python`. Now make symbolic
link to cloned Movelister folder with following and change `path_to_movelister`
to point to your cloned Movelister folder:
```
ln -s <path_to_movelister> movelister
```
Now in LibraOffice when you go to **Tools -> Macros -> Run Macro** and open **My
Macros**. You should see **movelister** as a listed macro package. Now open
**movelister** and select **main**. Then on the right you should see list of all
available macros which can be executed or mapped to keys.


#### Running macros from separate Python process
In project root folder, start LibreOffice Calc process with:
```
libreoffice templates/movelister_template.ods --accept="socket,host=localhost,port=2002;urp;StarOffice.ServiceManager"
```
This opens socket with port 2002 which Python process then connects. Then start
a separate Python process by running `main.py` with:
```
python main.py
```
This script should run without errors. If you see error messages, make sure the
socket is open or follow error message instructions.


### Windows
TODO: Write this again with better guidelines. To use LibreOffice Calc with a

socket open, you have to start LibreOffice using the parameter listed below.
For convenience's sake, you might want to include this parameter inside some
shortcut that starts LibreOffice.
```
--accept="socket,host=localhost,port=2002;urp;StarOffice.ServiceManager"
```
If you use command line to run scripts, it's the easiest to just use
LibreOffice's own installed version of Python to run any Python scripts.
Otherwise Python may have difficulties finding the important Uno library. In
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
Before running tests you need to set `LB_MV_BIN` environment variable to point
to the LibreOffice executable. This is used to run LibreOffice during test. On
linux for example:
```
export LB_MV_BIN="libreoffice"
```
and on Windows:
```
set MV_LB_BIN="C:\Program Files\LibreOffice 5\program\soffice.exe"
```

Test are located under test folder at the project root. Test suite opens a
headless LibreOffice instance with project template `.ods` file. Then between
each test the file is reopened. How to run tests depends your LibreOffice
installation. If you have separate Python that your LibreOffice is installation
is using. Then go to project root and run:
```
python -m unittest
```
If your LibreOffice has internal Python installation then. From project root you
need to traverse path to LibreOffice Python executable. In this case it might be
easier to make command line script to run tests. On Windows for example  make
following `.bat` at project root
file.
```
..\..\..\..\program\python -m unittest -v
```


## Resources
* [PyUno documentation](http://www.openoffice.org/udk/python/python-bridge.html).
* [Apache OpenOffice Developer's Guide](https://wiki.openoffice.org/wiki/Documentation/DevGuide/OpenOffice.org_Developers_Guide)
for main knowledge about OpenOffice UNO (Universal Network Objects) technology and how to use it.
* [LibreOffice 6.0 SDK API documentation](https://api.libreoffice.org/docs/idl/ref/index.html).
* [Jamie Boyle’s Cookbook](https://documenthacker.files.wordpress.com/2013/07/writing_documents-_for_software_engineers_v0002.pdf).
* [Christopher Bourez's](http://christopher5106.github.io/office/2015/12/06/openoffice-libreoffice-automate-your-office-tasks-with-python-macros.html)
	blog post about writing Python macros.
* [Jannie Theunissen's](https://onesheep.org/scripting-libreoffice-python/) blog
	post about scripting LibreOffice with Python.
* [Development enviroment setup using pyenv](https://gist.github.com/thekalinga/b74056272cb1afdabf529a332ff0f517).
