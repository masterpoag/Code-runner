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
        for directory in FOLDER_LOC:
            fileSearch(directory)
            return True

def fileSearch(directory):
    global FILE_LIST
    FOLDER_CONTENT = os.listdir(directory)
    for file in FOLDER_CONTENT:
        if "." in file:
            FILE_LIST.append(directory+file)
        else:
            fileSearch(directory+file+"/")

def fileCompiler(File):
    directory = File.rsplit("/",1)[0]+"/"
    fileName = File.split("/")[-1]
      






def filePicker():
    global FILE_LIST
    os.system('cls||clear')
    print("Pick the file you want to run. CTRL+C to quit")
    for file in FILE_LIST:
        print(f"{FILE_LIST.index(file)}) {file.split("/")[-1]}")
    user = input("")
    try:
        user = int(user,10)
    except:
        print("Make sure to pick a number. Press enter to return.")
        input("")
        filePicker()
    else:
        if(user <= len(FILE_LIST)):
            fileCompiler(FILE_LIST[user])
        else:    
            print("Make sure to pick a number listed. Press enter to return.")
            input("")
            filePicker()

def testing():
    pass

#testing()
if configReader():
    filePicker()