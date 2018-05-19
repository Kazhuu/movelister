# Movelister
TODO: Write description of the project.


## Dependancies
On Linux to enable Python for LibreOffice install:
```
sudo apt install libreoffice-script-provider-python
```


## Setup development environment
To have a good development environment and with debugging abilities. It's easier first to develop them using separate Python process which then connects to the external LibreOffice process. After you are done with the development, you can run working scripts inside of the LibreOffice process. [This Christopher Bourez's blog post](http://christopher5106.github.io/office/2015/12/06/openoffice-libreoffice-automate-your-office-tasks-with-python-macros.html) explains the idea.

### Linux
First start LibreOffice calc process with
```
libreoffice templates/movelister_template_v1.ods --accept="socket,host=localhost,port=2002;urp;StarOffice.ServiceManager"
```
Then start separate Python process and get access to LibreOffice process using opened socket.

### Windows
TODO: Write windows dev enviroment setup here.


## Resources
* [Apache OpenOffice Developer's Guide](https://wiki.openoffice.org/wiki/Documentation/DevGuide/OpenOffice.org_Developers_Guide) for main knowledge about OpenOffice UNO (Universal Network Objects) technology and how to use it.
* [LibreOffice 6.0 SDK API documentation](https://api.libreoffice.org/docs/idl/ref/index.html).
* [Jamie Boyle’s Cookbook](https://documenthacker.files.wordpress.com/2013/07/writing_documents-_for_software_engineers_v0002.pdf).
* [Python-UNO bridge](http://www.openoffice.org/udk/python/python-bridge.html) python library documentation.
* [unotools](https://pypi.org/project/unotools/#description) python package documentation.
* [Christopher Bourez's](http://christopher5106.github.io/office/2015/12/06/openoffice-libreoffice-automate-your-office-tasks-with-python-macros.html) blog post about writing Python macros.
* [Jannie Theunissen's](https://onesheep.org/scripting-libreoffice-python/) blog post about scripting LibreOffice with Python.
* [Development enviroment setup using pyenv](https://gist.github.com/thekalinga/b74056272cb1afdabf529a332ff0f517).
