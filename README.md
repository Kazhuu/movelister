# Movelister
Movelister is (or: will be) a tool for creating various types of in-depth notes about video game mechanics data in sheet form. This could include simple movelists, detailed mechanics notes for glitchers or other type of tables which model the limits of a game's potential interactivity.


## Dependancies
It's necessary for the user to install LibreOffice 5 to be able to use the Movelister scripts. Having Python installed is also a requirement. Python is automatically included in a LibreOffice installation on Windows but NOT on Linux, so on Linux the user may have to install Python separately.

On Linux, install following packages to enable Python for LibreOffice:
```
sudo apt install libreoffice-script-provider-python uno-libs3 python3-uno
```

## Setup development environment
To have a good development environment and with debugging abilities. It's easier to develop scripts using a separate Python process which then connects to an external LibreOffice process. After you are done with the development, you can run working scripts inside the LibreOffice process. [This Christopher Bourez's blog post](http://christopher5106.github.io/office/2015/12/06/openoffice-libreoffice-automate-your-office-tasks-with-python-macros.html) explains the idea.

### Linux
First, start LibreOffice Calc process with:
```
libreoffice templates/movelister_template_v1.ods --accept="socket,host=localhost,port=2002;urp;StarOffice.ServiceManager"
```
Then start a separate Python process and get access to LibreOffice process using the opened socket. Test the created connection by running `main.py` with:
```
python main.py
```
This script should run without errors. If you see error messages, make sure the socket is open.

### Windows
To use LibreOffice Calc with a socket open, you have to start LibreOffice using the parameter listed below. For convenience's sake, you might want to include this parameter inside some shortcut that starts LibreOffice.
```
--accept="socket,host=localhost,port=2002;urp;StarOffice.ServiceManager"
```
If you use command line to run scripts, it's the easiest to just use LibreOffice's own installed version of Python to run any Python scripts. Otherwise Python may have difficulties finding the important Uno library. In addition, you need to start running the scripts from the main Movelister directory so that Python can find any related Movelister-modules as well.

This part of the process can be made a bit faster by writing an own .bat file inside the Movelister main folder that starts main.py with LibreOffice's own Python executable that's usually situated in *LibreOffice 5/Program/*. For example:

```
..\..\..\..\program\python main.py
```

## For normal users

LibreOffice 5 has a specific directory where it searches for Python scripts - something along the lines of *LibreOffice 5/share/Scripts/python*. If you copy any Python scripts there, you are able to find & use them inside LibreOffice via *Tools -> Macros -> Run Macro...* It's not a bad idea to copy the entire Movelister directory inside *Scripts/Python* if you want to have access to all the scripts and ensure that Movelister finds all its dependencies too.

__Note:__ so far the scripts are designed to be used together with the Movelister template, so make sure that it's open in LibreOffice Calc before you run scripts or you most likely get some errors.

__Note 2:__ since this project is still at its early stages, the scripts don't offer a full functionality yet. Feel free to admire the template and give some feedback or ideas on it, though.


## Resources
* [PyUno documentation](http://www.openoffice.org/udk/python/python-bridge.html).
* [Apache OpenOffice Developer's Guide](https://wiki.openoffice.org/wiki/Documentation/DevGuide/OpenOffice.org_Developers_Guide) for main knowledge about OpenOffice UNO (Universal Network Objects) technology and how to use it.
* [LibreOffice 6.0 SDK API documentation](https://api.libreoffice.org/docs/idl/ref/index.html).
* [Jamie Boyle’s Cookbook](https://documenthacker.files.wordpress.com/2013/07/writing_documents-_for_software_engineers_v0002.pdf).
* [Christopher Bourez's](http://christopher5106.github.io/office/2015/12/06/openoffice-libreoffice-automate-your-office-tasks-with-python-macros.html) blog post about writing Python macros.
* [Jannie Theunissen's](https://onesheep.org/scripting-libreoffice-python/) blog post about scripting LibreOffice with Python.
* [Development enviroment setup using pyenv](https://gist.github.com/thekalinga/b74056272cb1afdabf529a332ff0f517).
