# Movelister
Movelister is - or will be - a versatile tool for creating various types of in-depth notes about video game character data in a sheet form. This could include simple movelists or other type of tables which map out the limits of a game's potential interactivity.


## Dependancies
LibreOffice installation is expected before these. On Windows LibreOffice installation includes Python installation but not on Linux. On Linux you also need to install Python 3 if not already available.


### Linux
On Linux to enable Python for LibreOffice install, if not already. Install following packages:
```
sudo apt install libreoffice-script-provider-python uno-libs3 python3-uno
```

### Windows
TODO: Write needed information about getting started if needed any.


## Setup development environment
To have a good development environment and with debugging abilities. It's easier first to develop them using separate Python process which then connects to external LibreOffice process. After you are done with the development, you can run working scripts inside of the LibreOffice process. [This Christopher Bourez's blog post](http://christopher5106.github.io/office/2015/12/06/openoffice-libreoffice-automate-your-office-tasks-with-python-macros.html) explains the idea.

### Linux
First start LibreOffice calc process with:
```
libreoffice templates/movelister_template_v1.ods --accept="socket,host=localhost,port=2002;urp;StarOffice.ServiceManager"
```
Then start separate Python process and get access to LibreOffice process using opened socket. Test created connection by running `main.py` with:
```
python main.py
```
This script should run without the errors. If you see error messages, make sure the socket is open.

### Windows
To use LibreOffice Calc with a socket open, you have to start LibreOffice using the parameter listed below. For convenience's sake, you might want to include this parameter inside a shortcut that starts LibreOffice.
```
--accept="socket,host=localhost,port=2002;urp;StarOffice.ServiceManager"
```
It's most convenient to use LibreOffice's own installed version of Python to run any Python scripts so that it can automatically find the important Uno library. In addition, you need to run Movelister-related scripts from the main Movelister directory so that it can find any useful modules related to it as well.

This part of the process can be made a bit faster by writing an own .bat file inside the Movelister main folder that starts main.py with LibreOffice's own Python executable that's usually situated in *LibreOffice 5/Program/*. For example:

```
..\..\..\..\program\python main.py
```

## Resources
* [Apache OpenOffice Developer's Guide](https://wiki.openoffice.org/wiki/Documentation/DevGuide/OpenOffice.org_Developers_Guide) for main knowledge about OpenOffice UNO (Universal Network Objects) technology and how to use it.
* [LibreOffice 6.0 SDK API documentation](https://api.libreoffice.org/docs/idl/ref/index.html).
* [Jamie Boyle’s Cookbook](https://documenthacker.files.wordpress.com/2013/07/writing_documents-_for_software_engineers_v0002.pdf).
* [Python-UNO bridge](http://www.openoffice.org/udk/python/python-bridge.html) python library documentation.
* [unotools](https://pypi.org/project/unotools/#description) python package documentation.
* [Christopher Bourez's](http://christopher5106.github.io/office/2015/12/06/openoffice-libreoffice-automate-your-office-tasks-with-python-macros.html) blog post about writing Python macros.
* [Jannie Theunissen's](https://onesheep.org/scripting-libreoffice-python/) blog post about scripting LibreOffice with Python.
* [Development enviroment setup using pyenv](https://gist.github.com/thekalinga/b74056272cb1afdabf529a332ff0f517).
