import os 
CONFIG_LAYOUT = f"""# Location of directories with code in them for more then 1 file sperate with commas.
Code/
# for code that requires being compiled they will be located here 
Compiled/
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
go
go build -o {{FILENAME}} {{FILE}}
rust
rustc -o {{FILENAME}} {{FILE}}
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
            return True

def filesearch(f):
    global FILE_LIST
    FOLDER_CONTENT = os.listdir(f)
    for i in FOLDER_CONTENT:
        if "." in i:
            FILE_LIST.append(f+i)
        else:
            filesearch(f+i+"/")

def filePicker():
    global FILE_LIST
    
    print("Pick the file you want to run. CTRL+C to quit")
    for i in FILE_LIST:
        print(f"{FILE_LIST.index(i)}) {i.split("/")[-1]}")
    user = input("")
    try:
        user = int(user,10)
    except:
        print("Make sure to pick a number. Press enter to return.")
        filePicker()
    else:
        if(user > len(FILE_LIST)-1):
            print("Make sure to pick a number listed. Press enter to return.")
            input("")
            filePicker()

def testing():
    pass

#testing()
if configReader():
    filePicker()