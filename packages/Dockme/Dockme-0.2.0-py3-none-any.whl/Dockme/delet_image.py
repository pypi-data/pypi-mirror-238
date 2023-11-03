import os


def del_image(image_name):
    try:
        os.system('docker rmi ' + image_name)
    except:
        print("Could not execute command")