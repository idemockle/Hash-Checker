# Hash Checker
A simple utility which provides a GUI for Python's built-in hashlib module and allows for simple checking of file checksums provided by web sites. I created this utility to learn the basics of working with PyQt. It is a very simple application consisting of only a single Python script, HashChecker.py, and the Windows executables were created using PyInstaller 3.2.1 with Python 3.5.3. 

## Using Hash Checker
### Windows
Download the appropriate zip file for your operating system (32 bit or 64 bit). Extract the downloaded zip file by right-clicking it and selecting "Extract All...". The *.exe file is a standalone program, not an installer. The Windows executables support the following algorithms: MD4, SHA1, SHA224, SHA256, SHA384, and SHA512.

### Python >=2.7 and >=3.5
Hash Checker is easy to run if you already have Python and PyQt5 installed. Simply run HashChecker.py from the command line by navigating to the appropriate directory and running the command "python HashChecker.py".

Hash Checker is compatible with Python 2 or 3, and has been tested with Python 2.7, 3.5, and 3.6, though it should work with earlier versions as well as long as an appropriate PyQt package is available.

Hash Checker was written using PyQt 5.6.0 and Qt 5.6.2. PyQt5 can be easily installed into your python environment using pip ("pip install pyqt") or conda ("conda install pyqt"). I have not tested Hash Checker with PyQt4, which is apparently a gigantic pain to get running on Windows, but I believe the only incompatibility is in the build() method, and it is marked in a comment.

The python script supports all available hashlib algorithms except for the shake algorithms. Most notably, that means that the SHA-3 and BLAKE2 algorithms are available when you run the script with Python 3.6 (or greater).