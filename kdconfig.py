import os

config_file = os.path.join(os.path.expanduser('~') , ".config/kdLaunchPad/config.json")
cmd =None
name = None

def to_dict():
    return{
        "cmd":cmd,
        "name":name
        }
def from_dict(conf):
    cmd = conf["cmd"]
    name = conf["name"]
    