import os


def del_container(container_name):
    try:
        os.system('docker rm ' + container_name)
    except:
        print("Could not execute command")