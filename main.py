import os,subprocess
CONFIG_LAYOUT = f"""# Location of directories with code in them for more then 1 file sperate with commas.
Code/
# for code that requires being compiled they will be located here 
Compiled/
# Compile commands change or add to what you use
# compiler arguments start
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
rs
rustc -o {{FILENAME}} {{FILE}}
# compiler arguments end
"""
compilerStart,compilerEnd = "# compiler arguments start\n","# compiler arguments end\n"
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
    config = open("config.cfg").readlines()
    start = config.index(compilerStart) + 1
    end = config.index(compilerEnd)
    configList = [x.strip() for x in config[start:end]]
    codingLangs = configList[::2]
    arguments = configList[1::2]
    found = False
    for fileExtension in codingLangs:
        if fileExtension == fileName.split(".")[-1].lower():
            found = True
            print(f"Found file extension in config it is a .{fileExtension} and its arguments are {arguments[codingLangs.index(fileExtension)]}")
            print(arguments[codingLangs.index(fileExtension)].replace(f"{{FILENAME}}",fileName.split(".")[0]+str(codingLangs.index(fileExtension))).replace(f"{{FILE}}",File))
            break
    if not found:
        print("Unknown file extension can't handle add it into config.cfg manually if you want run it")
      

def CMDRun(command,directory):
    # Run the command
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, cwd=directory)
    # Capture the output
    stdout, stderr = process.communicate()
    # Check if there were any errors
    if stderr:
        print("Error:", stderr)
    else:
        # Print the output
        print("Output:", stdout)



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

fileCompiler("Code/project/src/test.rs")

# if configReader():
#     filePicker()