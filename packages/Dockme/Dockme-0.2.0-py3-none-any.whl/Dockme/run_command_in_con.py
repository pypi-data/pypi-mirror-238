import os


def run_command(container_name, command):
    try:
        os.system('docker exec -it -d', container_name, ' bash')
        os.system(command)
        os.system('exit')
    except:
        print("Could not execute command")