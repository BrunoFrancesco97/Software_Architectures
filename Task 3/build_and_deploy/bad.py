#Python3 based build and deploy script
import sys
import platform
import subprocess

def launch():
    plat=platform.system()
    if plat == "Linux":
        subprocess.call(['sh', './build.sh'])
        subprocess.call(['sh', './deploy.sh'])
    else:
        if plat == "Windows":
            subprocess.call([r'build.bat'])
            subprocess.call([r'deploy.bat'])
        else:
            print("Platform "+plat+" not supported!")

if not sys.version_info.major == 3:
    print("Python 3.10 or higher is requested.")
    print("You are using Python {}.{}".format(sys.version_info.major, sys.version_info.minor))
    sys.exit(1)
else:
    launch()