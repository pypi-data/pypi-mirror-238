import os


def run_container(container_name, ports, image):
    try:
        if ports == None:
            os.system('docker run -it -d --name ' + container_name + ' ' + image)
        else:
            
           os.system('docker run -it -d -p ' + ports + ' --name ' + container_name + ' ' + image)
    except:
        print("Could not execute command")