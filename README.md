Kekulean
========
Introduction
------------
###What is this program?

The task of finding Kekulean structures (or perfect matchings from a graph theory perspective) in benzenoid graphs (also known as benzene patches, hexagonal systems, to name a few) is an easy-to-understand process but can be very time and labor consuming even with small graphs. On top of this problem, chemical graph theorists are often interested in finding the number of Clars and Fries face of the graph which are indictors of the strength of the chemical compound that the graph represents. Finding all this information accurately can be time consuming and is hard or even impossible to generalize as details seem to be dependent on the structure of the graph.
This program is capable of generating graphs, determining if it is Kekulean, find all possible perfect matchings, determine the Clars and Fries number of each structure and output the results to a PNG file for later review.

###Technical Details of the program

The program is written in Python and is entirely open-source to better help others in field quickly test graphs and find properties of them without the time-consuming effort that is involved in manually replicating the process.  This program is run using Python 2. YOu must have at least version 2.6 as that verison introduced multiprocessing
To run the program, run ‘Kekulean.py’ by double-clicking it or via the terminal/command line
There is one outside dependency that is not included with the .zip of the program. The Pillow library provides the functionally to create PNG of the results of the programs. Pillow is needed in order for the program to run.
For most users, the Clars-Fries differential that is calculated may seem foreign as it is a property that a research colleague invented and was interested in.  This is no reason to pay any attention to it.

Installation
------------
###LINUX

**Python**

The program is designed to run using Python 2 and is not tested for Python 3. Python should be installed by default on Linux machines but you can update your version of Python by downloading from https://www.python.org/download/.  You can also use: ```sudo apt-get install python``` to update to the latest version, if you are on an Ubuntu/Ubuntu-based system.
You can check if you Python installed and what version by typing python into the terminal. This will bring you into python’s interactive mode. You exit interactive mode by pressing Ctrl+D.

**Pillow**

Fedora, Debian/Ubuntu, and ArchLinux all come with Pillow installed in place of the Python Imaging Library (PIL).  Debian/Ubuntu systems can install Pillow using the terminal command: ```sudo apt-get install python-dev python-setuptools``` 

###MAC OSX

**Python**

The program is designed to run using Python 2 and is not tested for Python 3. Python should be installed by default on Mac OSX machines but you can update your version of Python by downloading from https://www.python.org/download/.  

You can check if you Python installed and what version by typing python into the terminal. This will bring you into python’s interactive mode. You exit interactive mode by pressing Ctrl+D.


**Pillow**

You can download the source from https://pypi.python.org/pypi/Pillow, extract it, and run python setup.py install from the terminal while in the same directory as the extracted files. If you have pip installed you can run: ```pip install Pillow``` in the terminal. If you do not have pip you can use: ```easy_install Pillow``` in the terminal to install Pillow

###Windows

**Python**

You can download a Windows installer from the https://www.python.org/download/ website. There are installers for both 32-bit and 64-bit processors. If you do not know what version you have (most likely you have 32-bit, especially on older machines), you should download the regular installer (the one that is not labeled as the X86-64 installer (This is the 64-bit processor one)).  If you encounter errors now or later, you may have installed the wrong version and should retry with to the other installer.  You can check to see if python installed, or is installed, by searching your computer for a program called IDLE. This a Python IDE that is packaged with Python and can be used to write and run Python programs.

**Pillow**

You can download a Pillow installer from https://pypi.python.org/pypi/Pillow/2.2.1#downloads and select an installer based on what version of Windows you are running (32-bit processor vs 64-bit processor) and what version of Python you are using (2.7 or 2.6; program is not tested for Python3).
Run the .exe file and follow the on screen instructions.

How to use this program
-----------------------
The program allows the user to analyze benzenoid graphs and determine properties such as whether a graph is Kekulean, the number of Kekulean structures, and the Clars and Fries numbers of the graph.  Input and textual output are given using a coordinate based on the faces of the graph and will be explained later on in this section. 

###Analyze graph from text file
The first option in the program is to read a graph from ‘graph.txt’ and determine properties of said graph. It will tell you the graph is Kekulean, the number of Kekulean structures, and the Clars and Fries numbers. It will ask the user how they want the structures organized and display user-specified graphs. It also outputs all the structures to two PNG files, each one ranked according to Clars numbers or Fries numbers. Please note that the outputted PNGs will overwrite older ones so you should back up any files you want to save.  

###Analyze random Kekulean graph
The second option creates a randomly generated Kekulean graph. The program then analyzes it much like the above mentioned option. Please note that the outputted PNGs will overwrite older ones so you should back up any files you want to save.  

###Create and test random graphs
The third option will create a user-specified number of randomly-generated graphs and then test to see if which ones are Kekulean or not.  Output is saved in the ‘Kekuleans.txt’ and ‘nonKekuleans.txt’ using the coordinate system that will be described later in this section.

###Create several Kekuleans
This fourth option creates a user-specified number of randomly-generated Kekulean graphs. It does not export the graphs to a PNG or text file.  This option is only recommend if you want to create a lot of graphs and find which one has the most Clars/Fries faces.

###Refresh Settings
Users can edit the properties that randomly generated graphs will have by editing ‘settings.txt’.  You should only change the numbers in the text file.  Normally this file is read only at the beginning of the program. If you change the numbers in ‘settings.txt’ and wish for your changes effect the program right away, selecting this option will update the random generation with the new settings mid-runtime.

###Other options
The other options listed, excluding quit, are used for the research purposes that come up while I wrote the program as part of undergraduate research.  They should be ignored and once the research program is over, will no longer be part of the program. If you are the research with me, then you know why they are there and you can use then it.

Contact
-------
For additional help, questions, or concerns or improvements you want made about this program, I can be reached at smorgasbordator@gmail.com. Please add Kekulean to the subject line for priority.
