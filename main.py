import os 
CONFIG_LAYOUT = f""" # Location of directories with code in them for more then 1 file sperate with commas.
Code/
# Compile commands change or add to what you use
c
gcc -o {{FILENAME}} {{FILE}}
c++
g++ -o {{FILENAME}} {{FILE}}
java
javac {{FILE}}
python
python -m py_compile {{FILE}}
c#
csc {{FILE}}
"""

FOLDER_LOC= 0
FILE_LIST = []

def configReader():
    global FOLDER_LOC,CONFIG_LAYOUT
    try:
        FOLDER_LOC = open("config.cfg").readlines()[1].strip().split(",")
    except:
        f = open("config.cfg", "w")
        f.write(CONFIG_LAYOUT)
        f.close()
        configReader()
    else:
        for i in FOLDER_LOC:
            filesearch(i)

def filesearch(f):
    global FILE_LIST
    print(f)
    FOLDER_CONTENT = os.listdir(f)
    for i in FOLDER_CONTENT:
        if "." in i:
            FILE_LIST.append(f+i)
        else:
            filesearch(f+i+"/")
configReader()
print(FILE_LIST)

# testing
# print(open("config.cfg").readlines()[1].split(","))