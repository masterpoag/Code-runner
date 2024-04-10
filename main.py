import os 
FOLDER_LOC= 0
FILE_LIST = []

def configReader():
    global FOLDER_LOC
    try:
        FOLDER_LOC = open("config.cfg").read()
    except:
        f = open("config.cfg", "w")
        f.write("Code/")
        f.close()
        configReader()
    else:
        filesearch(FOLDER_LOC)

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