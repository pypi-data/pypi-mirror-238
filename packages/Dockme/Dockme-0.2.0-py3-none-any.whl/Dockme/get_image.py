import os


def pull_image(image_name):
    try:
        os.system('docker pull ' + image_name)
    except:
        print("Could not execute command")