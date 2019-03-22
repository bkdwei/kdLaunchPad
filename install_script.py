import sys
import os
import shutil
from setuptools.command.install import install
class install_cmd(install):
    def run(self):
        install.run(self)
        if sys.platform =="win32" :
                path =  os.path.join(os.path.expanduser("~"), 'Desktop','kdLaunchPad.bat')
                print("copy windows's script in " + path)
                shutil.copyfile("script/kdLaunchPad.bat",path)
        elif sys.platform == "linux":
                path = '/usr/share/applications/kdLaunchPad.desktop'
                print("copy linux's desktop file in " + path)
                shutil.copyfile("script/kdLaunchPad.desktop",path)
               
