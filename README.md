# Password-Analysis-and-Storage-System 
[![Open in Gitpod (beta)](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/PASS21/Password-Analysis-and-Storage-System/) 
 [![Gradient](https://assets.paperspace.io/img/gradient-badge.svg)](https://console.paperspace.com/github/PASS21/Password-Analysis-and-Storage-System/blob/main/PasswordSystem.ipynb?clone=True) 

<!-- ![Jupyter](https://img.shields.io/badge/Made%20with-Jupyter-orange?style=for-the-badge&logo=Jupyter?style=for-the-badge&logo=Jupyter) -->
[![Made with Doom Emacs](https://img.shields.io/badge/Made_with-Doom_Emacs-blueviolet.svg?style=round&logo=GNU%20Emacs&logoColor=white)](https://github.com/hlissner/doom-emacs)    

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/PASS21/Password-Analysis-and-Storage-System/main)

### Todo:
- Add support for Firefox logins (currently impossible)

### Note: `Python` and `pip` have to be in PATH (it usually is for macOS/Linux, [here's how to add it to PATH in  Windows](https://www.makeuseof.com/python-windows-path) )
*If the system version of Python (on macOS) is too old, download a newer version of Python , either from the website or using `HomeBrew`*

*On Linux, use your package manager to update Python - **if** even that version is old, you may have to*
- Install  `git`, `gcc`,`make` and `build-essential` using your package manager
- Run `git clone https://github.com/python/cpython.git && cd cpython && ./configure --prefix /opt/python3.8 && make && make install && ln -s /opt/python3.8/bin/python3.8 /usr/bin/python3`

# How to get the code:
If you don't have Git:
- If you also do not have `winget` ,  get the [Latest WinGet release](https://github.com/microsoft/winget-cli/releases/download/v1.1.12653/Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle)
- `winget install git` ( if you don't have git) 

`git clone https://github.com/PASS21/Password-Analysis-and-Storage-System/ pass-cli`

` cd pass-cli`

` pip.exe install -U jupyter pandas sympy pwnedpasswords `

Then run the Jupyter Notebook or the Python file.

### If you want an executable file for Windows:
- Type this in Command Prompt: 
- `git clone https://github.com/PASS21/Password-Analysis-and-Storage-System PASS && cd PASS` (If you don't have the repo)
- then `pip install -U py2exe`
- Create a `setup.py` file having the following content:
```python
from distutils.core import setup
import py2exe
setup(console=['PasswordSystem.py'])
```
- Run `python setup.py py2exe`
- Wait for some time , then run `dist/PasswordSystem.exe`
