# Aspirobot
This program is a simulation of a vaccum cleaner trying to clean its environment.
The environment randomly generates dust and lost jewels.
The agent has to suck the dust and pick up the jewels.

## How to install
Tk/tcl graphics library is required. [Install instructions](https://tkdocs.com/tutorial/install.html)
```bash
git clone https://github.com/Nyckel/Aspirobot.git
```

## How to use
```
cd Aspirobot
python main.py
```

## Make an executable file
It's possible to create an executable file using [PyInstaller](https://www.pyinstaller.org/).
The executable can be produced using the following commands
```
pip install pyinstaller
pyinstaller main.spec
```
You will then find it in the "dist" folder. 
You can produce executable for all platforms although cross platform production is not possible.