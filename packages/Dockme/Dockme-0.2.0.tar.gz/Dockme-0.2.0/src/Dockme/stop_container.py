import os


def stop_container(container_name):
    try:
        os.system('docker stop ' + container_name)
    except:
        print("Could not execute command")