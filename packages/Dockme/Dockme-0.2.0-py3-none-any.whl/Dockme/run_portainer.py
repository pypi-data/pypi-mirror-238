import os


def run_portainer():
    try:

        os.system('docker run -it -d --name portainer_vorg -p 9000:9000 portainer')
        print('Status', True)
        print('Web_Port is 9000')
    except:
        print("Could not execute command")