import os


def ls_running_container():
    try:
        runnings = os.system('docker ps')
        return runnings
    except:
        print("Could not execute command")
        
def ls_container():
    try:
        containers = os.system('docker ps -a')
        return containers
    except:
        print("Could not execute command")

def ls_image():
    try:
        images = os.system('docker image list')
        return images
    except:
        print("Could not execute command")