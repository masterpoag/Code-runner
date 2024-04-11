import os,subprocess
CONFIG_LAYOUT = f"""# Location of directories with code in them for more then 1 file sperate with commas.
Code/
# for code that requires being compiled they will be located here 
Compiled/
# Compile commands change or add to what you use only files filled in this format will show up.
# compiler arguments start
c
gcc -o {{COMPILED_FOLDER+FILENAME}} {{FILE}}
c++
g++ -o {{COMPILED_FOLDER+FILENAME}} {{FILE}}
java
javac {{FILE}}
py
python -m {{FILE_W/O_TYPE}}
c#
csc {{FILE}}
go
go build -o {{COMPILED_FOLDER+FILENAME}} {{FILE}}
rs
cargo run {{FILE}}
# compiler arguments end
"""
compilerStart,compilerEnd = "# compiler arguments start\n","# compiler arguments end\n"
ignoreStart,ignoreEnd = "# ignored files start\n","# ignored files end\n"
FOLDER_LOC,compiledFolder,FILE_LIST  = 0,0,[]

def configReader():
    global FOLDER_LOC,CONFIG_LAYOUT,compiledFolder
    try:
        FOLDER_LOC= open("config.cfg").readlines()[1].strip().split(",")
        compiledFolder = open("config.cfg").readlines()[3].strip()
        print(compiledFolder)
    except:
        f = open("config.cfg", "w")
        f.write(CONFIG_LAYOUT)
        f.close()
        configReader()
            



def fileSearch(directory,config,codingLangs):
    global FILE_LIST
    FOLDER_CONTENT = os.listdir(directory)
    for file in FOLDER_CONTENT:
        if "." in file:
            found = False
            for lang in codingLangs:
                if file.split(".")[-1] in lang and file.split(".")[-1] != "o":
                    found = True
            if found:
                FILE_LIST.append(directory+file)           
        else:
            fileSearch(directory+file+"/",config,codingLangs)

def fileCompiler(File):
    global config,arguments,codingLangs,compiledFolder
    directory = File.rsplit("/",1)[0]+"/"
    fileName = File.split("/")[-1]
    fileType = File.split(".")[-1]
    found = False
    for fileExtension in codingLangs:
        if fileExtension == fileName.split(".")[-1].lower():
            found = True
            index = codingLangs.index(fileExtension)
            print(f"Found file extension in config it is a .{fileExtension} and its arguments are {arguments[index]}")
            shellCMD = arguments[index].replace(f"{{FILE_W/O_TYPE}}",fileName.split(".")[0]).replace(f"{{COMPILED_FOLDER+FILENAME}}",compiledFolder+fileName.split(".")[0]+str(index)).replace(f"{{FILE}}",File.split("/")[-1])
            CMDRun(shellCMD,directory)
            if fileType in "java":
                for file in os.listdir(directory):
                    if ".class" in file:
                        os.rename(directory+file, compiledFolder+file)
                        shellCMD = f"java {file.split(".")[0]}"
                        print(shellCMD)
                        CMDRun(shellCMD,compiledFolder)

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
    #os.system('cls||clear')
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
if __name__ == "__main__":
    configReader()
    config = open("config.cfg").readlines()
    start = config.index(compilerStart) + 1
    end = config.index(compilerEnd)
    configList = [x.strip() for x in config[start:end]]
    codingLangs = configList[::2]
    arguments = configList[1::2]
    for i in FOLDER_LOC:
        fileSearch(i,config,codingLangs)
    filePicker()