# PyGuide

The PyGuide software is the Python version of the original Guide software written in C++. Python was choosen in order to speed up developement process compared to C++, however, right now only a few of the original fonctionnalities where migrated to Python. Those include : activity management, membreship management and a simplified facturation module. 

## Getting started

This software is programmed with PyQt5 and Python 3.6 in order to make it portable however only Microsoft Window 10 is fully supported and tested. For this reason, only the windows installation instructions are provided even if it should be possible to install and run this software on Linux or MacOS. 

### Prerequisites

This software require the following software to be installed : 
* Python 3.6 or newer
* PyQt 5.10.0 or newer

The Windows Python 3 distribution can be downloaded there : https://www.python.org.

Once Python 3 is installed, open the Command Prompt and execute the following line : 
```
pip3 install PyQt5
```

Some module (i.e statistics PDF generation) also need a LaTeX distribution installed. If you are not familiar with LaTeX the use of the MikTex distribution for Windows is recommended (https://miktex.org). The base installation should be enough to use this software however it might not include all the required packages therefore the option to install missing packages sould be actived. 

### Installation

When all the prerequisites are installed this software does not need any installation steps. It is possible to execute the software directly from any location on the computer with the following Command Prompt command :  
```
python3 /path/to/main.py
```

## Contribute

Feel free to contribute to this software. 

## Author

**Samuel Prince-Drouin** 2017-2018

## License

This project is made available under GPL 3 - see [LICENSE.md](LICENSE.md) file for details. 
