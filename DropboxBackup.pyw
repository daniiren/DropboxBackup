from datetime import datetime, date
import os
import sys
import shutil
import time
import filecmp

sys.setrecursionlimit(10**6) # We set the recursion limin to 1.000.000 (because python by default has a smaller recursion limit)

inputPath = "C:\\Users\\...\\Dropbox"
inputPath = inputPath.replace("\\", "/") + "/"
outputPath = "D:\\Documents\\Dropbox"
outputPath = outputPath.replace("\\", "/") + "/"
listWithChanges = []

def DropboxBackup(inputPath, outputPath) :
    filesNameOfInput = []
    filesNameOfOutput = []

    # If an item in input path is a file then call it self (recursion) 
    # otherwise append the file name to an array, so we can make some checks later.
    for item in os.listdir(inputPath) :
        if (item != ".dropbox.cache" and item != ".dropbox" and item != "desktop.ini") :
            if (os.path.isdir(inputPath + item)) :
                DropboxBackup(inputPath + item + "/", outputPath + item + "/")
            filesNameOfInput.append(item)

    # Check if the output path that we want to create already exist,
    # if exist then check every file in it and delete files that dont exist 
    # or entire folders (with files or not in them) in the input path (input path = primary path) 
    # and append files were already exist in the input path to filesNameOfOutput array
    if (os.path.exists(outputPath)) :                   
        for item in os.listdir(outputPath) : 
            if (item != "logFileOfDropboxBackup.txt") :           
                if (item not in filesNameOfInput) :         
                    if (os.path.isdir(outputPath + item)) : # Check if the path is a directory,
                        shutil.rmtree(outputPath + item)    # if it is, the delete it (with files or not in it)
                        tempVar = "Deleted folder : ", outputPath + item, "\n"
                        listWithChanges.append(''.join(tempVar))
                    else :
                        os.remove(outputPath + item)        # if is not a directory then delete the file
                        tempVar = "Deleted file : ", outputPath + item, "\n"
                        listWithChanges.append(''.join(tempVar))
                else :
                    if not (os.path.isdir(outputPath + item)) : 
                        if not (filecmp.cmp(outputPath + item, inputPath + item)) : # We compare byte by byte the same name files
                            os.remove(outputPath + item)                            # so we can be as sure as we can if are really the same files or not
                        else :                                                      
                            filesNameOfOutput.append(item)
                    else :
                        filesNameOfOutput.append(item)
    else :  # If the output path dont exist, we create it
        try :
            os.makedirs(outputPath)
            tempVar = "Created folder(s) : ", outputPath, "\n"
            listWithChanges.append(''.join(tempVar))
        except OSError :
            print("Error")

    for item in filesNameOfInput :  # Copy files from the input path that dont exist in the output path
        if (item not in filesNameOfOutput) :
            shutil.copy(inputPath + item, outputPath + item)
            tempVar = "Copied file from : ", inputPath + item, "\nto : ", outputPath + item, "\n"
            listWithChanges.append(''.join(tempVar))

while (True) :
    if (os.path.exists("D:/Documents/Dropbox/logFileOfDropboxBackup.txt")) :
        logFile = open("D:/Documents/Dropbox/logFileOfDropboxBackup.txt", "a")

        try :
            DropboxBackup(inputPath, outputPath)
            now = datetime.now()
            today = date.today()

            nowFormater = now.strftime("%H:%M:%S")
            todayFormated = today.strftime("%d/%m/%y")

            logFile.write(todayFormated)
            logFile.write(" ")
            logFile.write(nowFormater)
            logFile.write("\n")

            if (len(listWithChanges)) :
                for item in listWithChanges :
                    logFile.write(str(item))
                logFile.write("All ok, all files are backed up.\n\n")
            else :
                logFile.write("All ok, all files are backed up. (No changes needed)\n\n")
            listWithChanges.clear()
        except IOError as e:
            now = datetime.now()
            today = date.today()

            nowFormater = now.strftime("%H:%M:%S")
            todayFormated = today.strftime("%d/%m/%y")

            logFile.write(todayFormated)
            logFile.write(" ")
            logFile.write(nowFormater)
            logFile.write("\n")
            logFile.write(str(e))   # In case of some error we write it in log file
            logFile.write("\n\n")

        logFile.close()
        time.sleep(21600)           # We are "saying" to our script to sleep for 6 hour (21600 sec) before it start run again
