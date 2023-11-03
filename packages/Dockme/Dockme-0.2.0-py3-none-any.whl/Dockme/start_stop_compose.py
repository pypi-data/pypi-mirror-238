import os

def run_compose(path):
    try:
        os.system('cd', path, ' && docker-compose up -d')
        
    except:
        print("Could not execute command")
        
def stop_compose(path):
    try:
        os.system('cd', path, ' && docker-compose down')
        
    except:
        print("Could not execute command")