import os
import subprocess
districtNames = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
startingNum = 401000000

for index, elem in enumerate(districtNames):
    subprocess.shell=True
    os.system("start cmd /c districtStarter.bat " + str(districtNames[index].upper()) + " " + str(startingNum))
    startingNum = startingNum + 1000000