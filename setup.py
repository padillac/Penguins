#This script will automatically use Pip to install any dependencies that you don't already have installed
import subprocess
import sys



def pipinstall(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])
def aptinstall(package):
    subprocess.call(['sudo', "apt", "install", package])



aptinstall('python3-tk')
pipinstall('mttkinter')
