import os
import shutil
import time
try:
    os.system('pyinstaller C64Compiler.py --onefile -n "C64Compiler"')
    shutil.rmtree('build')
    shutil.move("dist/C64Compiler.exe", "C64Compiler.exe")
    os.rmdir("dist")
except:
    print("ERROR WHILE BUILDING!")
    time.sleep(2)
    exit()
print("build successful!")
time.sleep(2)
exit()